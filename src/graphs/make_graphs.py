import pandas as pd
import pathlib as path
import plotly.express as px
import plotly.graph_objects as go


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
        maximum_dict[restaurant] = 0
        minimum_dict[restaurant] = 0
        for col in star_cols:
            diff = restaurant_df[col].diff()
            
            try:
                maximum_changement = int(diff.max())
                minimum_changement = int(diff.min())
            except ValueError:
                print(f"diff error case: {restaurant} {diff}")
            i = 1
            while maximum_changement > 0 and maximum_changement == abs(minimum_changement):
                # get next highest and lowest 
                maximum_changement = int(diff.nlargest(i+1).iloc[i])
                minimum_changement = int(diff.nsmallest(i+1).iloc[i])
                i += 1
                
            if maximum_dict[restaurant] < maximum_changement and maximum_changement != abs(minimum_changement):
                maximum_dict[restaurant] = maximum_changement
            if minimum_dict[restaurant] > minimum_changement and maximum_changement != abs(minimum_changement):
                minimum_dict[restaurant] = minimum_changement

    max_values = pd.DataFrame(list(maximum_dict.items()), columns=['name', 'max_value'])
    max_values = max_values.sort_values('max_value')
    max_values = max_values[max_values['max_value'] > threshold]
    
    min_values = pd.DataFrame(list(minimum_dict.items()), columns=['name', 'min_value'])
    min_values = min_values[min_values['min_value'] < -threshold]
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
        
        
        r_df['date'] = pd.to_datetime(r_df['date'], format='mixed')
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
        
        

# min_values, max_values = find_anomalies(df, threshold=1)
# restaurants = pd.concat([min_values, max_values], ignore_index=True)
# restaurants = restaurants['name'].unique()
# plot_data(df, restaurants)
make_sankey_plot(df)
