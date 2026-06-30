import pandas as pd
import pathlib as path
import plotly.express as px


PATH = path.Path(__file__).parents[2]

CSV_PATH = PATH / 'data' / 'raw' / 'firstcrawl.csv'
PNG_PATH = PATH / 'data' / 'graphs' / 'interesting'

def find_anomalies(df):
    # get a list of restaurants in the dataframe by unique name
    all_unique_restaurants = df['name'].unique()
    star_cols = ['5 stars', '4 stars', '3 stars', '2 stars', '1 stars']
    for restaurant in all_unique_restaurants:
        restaurant_df = df[df['name'] == restaurant]
        
        for col in star_cols:
            diff = restaurant_df[col].diff()
            decrease_diff = diff[diff < 0]
            for diff in decrease_diff:
                date = restaurant_df.loc[diff.index, 'date']
                print(f"{restaurant} - {col} - {date}")
                print(decrease_diff)

def plot_data(df):
    # get a list of restaurants in the dataframe by unique name
    all_unique_restaurants = df['name'].unique()

    # print(all_unique_restaurants)
    for restaurant in all_unique_restaurants:
        # drop restaurant if there are less than 3 entries
        if len(df[df['name'] == restaurant]) < 3:
            print(f"The restaurant named {restaurant} was dropped, because only {len(df[df['name'] == restaurant])} entries are saved.")
            continue
        # get the measurements for this restaurant in its own dataframe
        r_df = df[df['name'] == restaurant]
        r_df['date'] = pd.to_datetime(r_df['date'], format='mixed')
        # Sort by date (critical for line graphs!)
        r_df = r_df.sort_values('date')
        
        # Reshape data
        r_df_long = r_df.melt(id_vars=['date'],
                    value_vars=['5 stars', '4 stars', '3 stars', '2 stars', '1 stars'],
                    var_name='Star Rating',
                    value_name='Count')
        # print(restaurant)
        # print(r_df_long)
        fig = px.line(r_df_long, x='date', y='Count', color='Star Rating',
            title=f'{restaurant}',
            labels={'date': 'Date', 'Count': 'Number of stars'},
            height=600, width=1000)
        fig.write_html(PNG_PATH / (restaurant.replace('/', '-') + '.html'))
        break


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
# print(len(df[df['name'] == 'Trattoria Momo, Bochum Stadionring 9']))
plot_data(df)
#find_anomalies(df)
