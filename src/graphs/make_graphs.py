import pandas as pd
import pathlib as path
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


PATH = path.Path(__file__).parents[2]

CSV_PATH = PATH / 'data' / 'raw' / 'firstcrawl.csv'
TOTAL_COUNT_PNG_PATH = PATH / 'data' / 'graphs' / 'interesting_total_count'
DIFF_PNG_PATH = PATH / 'data' / 'graphs' / 'interesting_differences'
GENERAL_PNG_PATH = PATH / 'data' / 'graphs' / 'general'


def find_anomalies(df, threshold):
    # get a list of restaurants in the dataframe by unique name

    all_unique_restaurants = df['name'].unique()
    maximum_dict = dict()
    minimum_dict = dict()

    star_cols = ['5 stars', '4 stars', '3 stars', '2 stars', '1 stars']
    for restaurant in all_unique_restaurants:
        restaurant_df = df[df['name'] == restaurant]
        # print(restaurant_df)
        # skip if this restaurant has less than 3 entries
        if len(restaurant_df) < 3:
            continue
        maximum_dict[restaurant] = 0
        minimum_dict[restaurant] = 0
        for col in star_cols:
            diff = restaurant_df[col].diff()
            
            try:
                maximum_changement = int(diff.max())
                max_idx = int(diff.idxmax())
                minimum_changement = int(diff.min())
                min_idx = int(diff.idxmin())
                
            except ValueError:
                print(f"diff error case: {restaurant} {diff}")
            i = 1
            star = int(col.split(' ')[0])
            min_value = restaurant_df[col].loc[min_idx]
            # if the minimum value is the star value, then look for scraping error pattern
            position = restaurant_df.index.get_loc(min_idx)
            prev_position = restaurant_df.index[position-1]
            prev_value = restaurant_df[col].loc[prev_position]
            try:
                next_position = restaurant_df.index[position +1]            
                next_value = restaurant_df[col].loc[next_position]
            except:
                # print(f"Error occured, end of list? {restaurant}\n{restaurant_df}")
                next_value = prev_value
            while minimum_changement < 0 and min_value == star and (prev_value != star or next_value != star):                    
                # while we have this pattern get the next
                # get next highest and lowest 
                maximum_changement = diff.nlargest(i+1).iloc[i]
                # print(maximum_changement)
                if pd.isna(maximum_changement):
                    maximum_changement = 0
                else:    
                    maximum_changement = int(maximum_changement)
                    
                minimum_changement = diff.nsmallest(i+1).iloc[i]
                min_idx = diff.nsmallest(i+1).index[i]
                # print(minimum_changement)
                if pd.isna(minimum_changement):
                    minimum_changement = 0
                else:    
                    minimum_changement = int(minimum_changement)

                i += 1
                position = restaurant_df.index.get_loc(min_idx)
                prev_position = restaurant_df.index[position-1]
                prev_value = restaurant_df[col].loc[prev_position]
                try:
                    next_position = restaurant_df.index[position +1]
                    next_value = restaurant_df[col].loc[next_position]
                except:
                    # print(f"Error occured, end of list? {restaurant}")
                    next_value = prev_value
                    
                    
            # save the maximum and minimum change for all cols
            if maximum_dict[restaurant] < maximum_changement:
                maximum_dict[restaurant] = maximum_changement
            if minimum_dict[restaurant] > minimum_changement:
                minimum_dict[restaurant] = minimum_changement

    max_values = pd.DataFrame(list(maximum_dict.items()), columns=['name', 'max_value'])
    max_values = max_values.sort_values('max_value')
    max_values = max_values[max_values['max_value'] > threshold] # only save the restaurants over the given threshold
    
    min_values = pd.DataFrame(list(minimum_dict.items()), columns=['name', 'min_value'])
    min_values = min_values[min_values['min_value'] < 0]
    min_values = min_values.sort_values('min_value')
    return min_values, max_values

def plot_data(df, restaurants):
    # get a list of restaurants in the dataframe by unique name

    for restaurant in restaurants:
        # drop restaurant if there are less than 3 entries
        if len(df[df['name'] == restaurant]) < 3:
            print(f"The restaurant named {restaurant} was dropped, because only {len(df[df['name'] == restaurant])} entries are saved.")
            continue
        # get the measurements for this restaurant in its own dataframe
        r_df = df[df['name'] == restaurant]
        star_cols = ['5 stars', '4 stars', '3 stars', '2 stars', '1 stars']
        
        r_df.loc[:, 'date'] = pd.to_datetime(r_df['date'], format='mixed')
        #r_df['date'] = pd.to_datetime(r_df['date'], format='mixed')
        # Sort by date (critical for line graphs!)
        r_df = r_df.sort_values('date')
        
        # Reshape data
        r_df_long = r_df.melt(id_vars=['date'],
                    value_vars=['5 stars', '4 stars', '3 stars', '2 stars', '1 stars'],
                    var_name='Star Rating',
                    value_name='Count')
        fig = px.line(r_df_long, x='date', y='Count', color='Star Rating',
            title=f'{restaurant} - Total Count of Ratings',
            labels={'date': 'Date', 'Count': 'Number of stars'},
            height=600, width=1000)
        fig.write_html(TOTAL_COUNT_PNG_PATH / (restaurant.replace('/', '-') + '.html'))
        
        # also plot the differences
        r_diff_df = r_df
        r_diff_df[star_cols] = r_diff_df[star_cols].diff()
        r_df['date'] = pd.to_datetime(r_df['date'], format='mixed')
        # Sort by date (critical for line graphs!)
        r_df = r_df.sort_values('date')
        
        # Reshape data
        r_df_long = r_df.melt(id_vars=['date'],
                    value_vars=['5 stars', '4 stars', '3 stars', '2 stars', '1 stars'],
                    var_name='Star Rating',
                    value_name='Count')
        fig = px.line(r_df_long, x='date', y='Count', color='Star Rating',
            title=f'{restaurant} - Changement of Reviews',
            labels={'date': 'Date', 'Count': 'Number of added or deleted stars'},
            height=600, width=1000)
        fig.write_html(DIFF_PNG_PATH / (restaurant.replace('/', '-') + '.html'))



def make_sankey_plot(df):
    min_values, max_values = find_anomalies(df, threshold=0)
    total_restaurants = len(df['name'].unique())
    number_with_deletions = len(min_values)
    number_with_additions = len(max_values) - 1
    add_1 = len(max_values[max_values['max_value'] < 2])
    add_2_4 = len(max_values[(max_values['max_value'] >= 2) & (max_values['max_value'] < 5)])
    add_5_9 = len(max_values[(max_values['max_value'] >= 5) & (max_values['max_value'] < 10)])
    add_10_14 = len(max_values[(max_values['max_value'] >= 10) & (max_values['max_value'] < 15)])
    add_15_19 = len(max_values[(max_values['max_value'] >= 15) & (max_values['max_value'] < 20)])
    add_over_20 = len(max_values[(max_values['max_value'] >= 20)])
    
    delete_1 = len(min_values[(min_values['min_value'] > -2)])
    delete_2_4 = len(min_values[(min_values['min_value'] <= -2) & (min_values['min_value'] > -5)])
    delete_5_9 = len(min_values[(min_values['min_value'] <= -5) & (min_values['min_value'] > -10)])
    delete_10_19 = len(min_values[(min_values['min_value'] <= -10) & (min_values['min_value'] > -20)])
    delete_20_49 = len(min_values[(min_values['min_value'] <= -20) & (min_values['min_value'] > -50)])
    delete_over_50 = len(min_values[(min_values['min_value'] <= -50)])
    print(number_with_additions, add_1, add_2_4, add_5_9, add_10_14, add_15_19, add_over_20) 
    fig = go.Figure(data=[go.Sankey(
        node = dict(
          thickness = 5,
          line = dict(color = "green", width = 0.1),
          label = ["Total", "With New Reviews", "Without New Reviews", "One New Review", "2-4 New Reviews", "5-9 New Reviews", "10-14 New Reviews"],
          color = "blue"
        ),
        link = dict(
            
          # indices correspond to labels
          source = [0, 0, 1, 1, 1, 1], 
          target = [1, 2, 3, 4, 5, 6],
          value = [number_with_additions, total_restaurants - number_with_additions, add_1, add_2_4, add_5_9, add_10_14]
      ))])

    fig.write_html(GENERAL_PNG_PATH / 'restaurants_with_new_reviews.html')
    

    fig = go.Figure(data=[go.Sankey(
        node = dict(
          thickness = 5,
          line = dict(color = "green", width = 0.1),
          label = ["Total", "With New Deletions", "Without New Deletions", "One New Deletion", "2-4 New Deletions", "5-9 New Deletions", "10-19 New Deletions", "20-49 New Deletions", "50+ New Deletions"],
          color = "blue"
        ),
        link = dict(
            
          # indices correspond to labels
          source = [0, 0, 1, 1, 1, 1, 1, 1], 
          target = [1, 2, 3, 4, 5, 6, 7, 8],
          value = [number_with_deletions, total_restaurants - number_with_deletions, delete_1, delete_2_4, delete_5_9, delete_10_19, delete_20_49, delete_over_50]
      ))])
    print(min_values)
    print(total_restaurants, number_with_deletions, delete_1)
    fig.write_html(GENERAL_PNG_PATH / 'restaurants_with_deletions.html')
    
    
    
def check_for_note(df, deletion_restaurants):
    """
    Function to check how many restaurants have a note about deletions, how many of the ones with deletions have a note.
    """
    

    total_number_of_restaurants = len(df['name'].unique())

    df_latest = df.drop_duplicates(subset=['name'], keep='last')
    notice_buckets = df_latest['notice'].value_counts()
    custom_order = ['101 to 150 reviews removed due to defamation complaints.', '51 to 100 reviews removed due to defamation complaints.', '21 to 50 reviews removed due to defamation complaints.', '11 to 20 reviews removed due to defamation complaints.', 'Six to ten reviews removed due to defamation complaints.', 'Two to five reviews removed due to defamation complaints.']
    #print(notice_buckets)
    notice_buckets = notice_buckets.reindex(custom_order)
    
    #print(notice_buckets)
    # Bar width in dots
    bar_width = 10

    # Calculate grid dimensions
    num_rows = int(np.ceil(total_number_of_restaurants / bar_width))

    # Create a grid to track which dot belongs to which bucket
    grid = np.full((num_rows, bar_width), None, dtype=object)

    # Fill the grid: colored dots on top, grey on bottom
    dot_index =  total_number_of_restaurants

    # Top rows: colored dots (one bucket at a time, left to right, top to bottom)
    for bucket_name in notice_buckets.index:
        bucket_count = notice_buckets[bucket_name]
        for i in range(bucket_count):
            if dot_index > 0:
                row = num_rows - 1 - (dot_index // bar_width)
                col = dot_index % bar_width
                grid[row, col] = bucket_name
                dot_index -= 1

    # Bottom rows: grey dots (remaining)
    for row in range(num_rows):
        for col in range(bar_width):
            if grid[row, col] is None and dot_index > 0:
                grid[row, col] = 'untracked'
                dot_index -= 1

    # Define colors for each bucket
    unique_buckets = list(notice_buckets.index)
    colors_palette = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ]
    color_map = {bucket: colors_palette[i % len(colors_palette)] for i, bucket in enumerate(unique_buckets)}
    color_map['untracked'] = '#cccccc'  # Grey for untracked

    # Extract x, y, color, and hover text for scatter plot
    x_coords = []
    y_coords = []
    colors = []
    hover_texts = []

    for row in range(num_rows):
        for col in range(bar_width):
            if grid[row, col] is not None:
                x_coords.append(col)
                y_coords.append(row)
                bucket = grid[row, col]
                colors.append(color_map[bucket])
                if bucket == 'untracked':
                    hover_texts.append('No deleted reviews')
                else:
                    hover_texts.append(f'{bucket} deleted reviews')

    # Create scatter plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_coords,
        y=y_coords,
        mode='markers',
        marker=dict(
            size=10,
            color=colors,
            line=dict(width=1, color='white')
        ),
        text=hover_texts,
        hovertemplate='<b>%{text}</b><extra></extra>',
        showlegend=False
    ))

    # Update layout
    fig.update_layout(
        title=f'Distribution of {total_number_of_restaurants} Restaurants by Deleted Reviews given by notice.',
        xaxis=dict(
            range=[-0.5, bar_width - 0.5],
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            autorange='reversed'
        ),
        plot_bgcolor='white',
        hovermode='closest',
        width=400,
        height=150 + (num_rows * 30)
    )


    # Create custom legend
    legend_traces = []
    for bucket in unique_buckets:
        count = notice_buckets[bucket]
        legend_traces.append(
            go.Scatter(
                x=[None], y=[None],
                mode='markers',
                marker=dict(size=10, color=color_map[bucket], line=dict(width=1, color='white')),
                name=f'{bucket.split('reviews')[0]} ({count})',
                showlegend=True
            )
        )

    # Add grey dot for untracked
    untracked_count = total_number_of_restaurants - notice_buckets.sum()
    legend_traces.append(
        go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(size=10, color='#cccccc', line=dict(width=1, color='white')),
            name=f'No Deletions ({untracked_count})',
            showlegend=True
        )
    )

    # Add legend traces to figure
    for trace in legend_traces:
        fig.add_trace(trace)

    fig.write_html(GENERAL_PNG_PATH / 'gridplot-notice-deletions.html')


def make_gridplot_tracked_deletions(df, min_values):
    """
    Function to check how many restaurants have a note about deletions, how many of the ones with deletions have a note.
    """
    #print(min_values)
    delete_1 = len(min_values[(min_values['min_value'] > -2)])
    delete_2_5 = len(min_values[(min_values['min_value'] <= -2) & (min_values['min_value'] >= -5)])
    delete_6_10 = len(min_values[(min_values['min_value'] < -5) & (min_values['min_value'] >= -10)])
    delete_11_20 = len(min_values[(min_values['min_value'] < -10) & (min_values['min_value'] >= -20)])
    delete_21_50 = len(min_values[(min_values['min_value'] < -20) & (min_values['min_value'] >= -50)])
    delete_51_100 = len(min_values[(min_values['min_value'] < -50) & (min_values['min_value'] >= -100)])
    delete_101_150 = len(min_values[(min_values['min_value'] < -100) & (min_values['min_value'] >= -150)])
    

    total_number_of_restaurants = len(df['name'].unique())

    # df_latest = df.drop_duplicates(subset=['name'], keep='last')
    notice_buckets = pd.DataFrame({
        'bucket': ['101 to 150', '51 to 100', '21 to 50', '11 to 20', 'Six to ten', 'Two to five', 'one'],
        'count': [delete_101_150, delete_51_100, delete_21_50, delete_11_20, delete_6_10, delete_2_5, delete_1]
        })
    
    print(notice_buckets)
    # Bar width in dots
    bar_width = 10

    # Calculate grid dimensions
    num_rows = int(np.ceil(total_number_of_restaurants / bar_width))

    # Create a grid to track which dot belongs to which bucket
    grid = np.full((num_rows, bar_width), None, dtype=object)

    # Fill the grid: colored dots on top, grey on bottom
    dot_index =  total_number_of_restaurants

    # Top rows: colored dots (one bucket at a time, left to right, top to bottom)
    for bucket_name in notice_buckets['bucket']:
        print(bucket_name)
        bucket_count = notice_buckets.loc[notice_buckets['bucket'] == bucket_name, 'count'].values[0]
        for i in range(bucket_count):
            if dot_index > 0:
                row = num_rows - 1 - (dot_index // bar_width)
                col = dot_index % bar_width
                grid[row, col] = bucket_name
                dot_index -= 1

    # Bottom rows: grey dots (remaining)
    for row in range(num_rows):
        for col in range(bar_width):
            if grid[row, col] is None and dot_index > 0:
                grid[row, col] = 'untracked'
                dot_index -= 1

    # Define colors for each bucket
    unique_buckets = list(notice_buckets['bucket'])
    print(unique_buckets)
    colors_palette = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ]
    color_map = {bucket: colors_palette[i % len(colors_palette)] for i, bucket in enumerate(unique_buckets)}
    color_map['untracked'] = '#cccccc'  # Grey for untracked

    # Extract x, y, color, and hover text for scatter plot
    x_coords = []
    y_coords = []
    colors = []
    hover_texts = []

    for row in range(num_rows):
        for col in range(bar_width):
            if grid[row, col] is not None:
                x_coords.append(col)
                y_coords.append(row)
                bucket = grid[row, col]
                colors.append(color_map[bucket])
                if bucket == 'untracked':
                    hover_texts.append('No deleted reviews')
                else:
                    hover_texts.append(f'{bucket} deleted reviews')

    # Create scatter plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_coords,
        y=y_coords,
        mode='markers',
        marker=dict(
            size=10,
            color=colors,
            line=dict(width=1, color='white')
        ),
        text=hover_texts,
        hovertemplate='<b>%{text}</b><extra></extra>',
        showlegend=False
    ))

    # Update layout
    fig.update_layout(
        title=f'Distribution of {total_number_of_restaurants} Restaurants by tracked Deleted Reviews.',
        xaxis=dict(
            range=[-0.5, bar_width - 0.5],
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            autorange='reversed'
        ),
        plot_bgcolor='white',
        hovermode='closest',
        width=400,
        height=150 + (num_rows * 30)
    )


    # Create custom legend
    legend_traces = []
    for bucket_name in unique_buckets:
        count = notice_buckets.loc[notice_buckets['bucket'] == bucket_name, 'count'].values[0]
        legend_traces.append(
            go.Scatter(
                x=[None], y=[None],
                mode='markers',
                marker=dict(size=10, color=color_map[bucket_name], line=dict(width=1, color='white')),
                name=f'{bucket_name.split('reviews')[0]} ({count})',
                showlegend=True
            )
        )

    # Add grey dot for untracked
    untracked_count = total_number_of_restaurants - notice_buckets['count'].sum()
    legend_traces.append(
        go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(size=10, color='#cccccc', line=dict(width=1, color='white')),
            name=f'No Deletions ({untracked_count})',
            showlegend=True
        )
    )

    # Add legend traces to figure
    for trace in legend_traces:
        fig.add_trace(trace)

    fig.write_html(GENERAL_PNG_PATH / 'gridplot-tracked-deletions.html')


df = pd.read_csv(CSV_PATH)
# data cleaning for the line with stashed changes
df = df[df.name != '>>>>>>> Stashed changes']

# do data cleaning for when the stars are saved as strings
star_cols = ['5 stars', '4 stars', '3 stars', '2 stars', '1 stars']
for col in star_cols:
    try:
        df[col] = df[col].astype(str).str.replace(',', '').astype(float).astype(int)
    except ValueError:
        print(df[col])
        
        
## get the restaurants with changements
min_values, max_values = find_anomalies(df, threshold=1)
print(f"len(max_values) {len(max_values)}, len(min_values): {len(min_values)}")
print(min_values)
restaurants = pd.concat([min_values, max_values], ignore_index=True)
restaurants = restaurants['name'].unique()
plot_data(df, restaurants)


deletion_restaurants, _ = find_anomalies(df, threshold=0)
check_for_note(df, deletion_restaurants)
make_gridplot_tracked_deletions(df, deletion_restaurants)


# make sankey plot
make_sankey_plot(df)
