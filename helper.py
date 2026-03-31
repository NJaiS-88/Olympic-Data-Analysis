def medal_tally(df):
    medal_tally = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal']);
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                              ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'overall')
    county = df['region'].dropna().unique()
    country = county.tolist()
    country.sort()
    country.insert(0, 'overall')
    return years, country

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'overall' and country == 'overall':
        temp_df = medal_df
    if year == 'overall' and country != 'overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'overall' and country == 'overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'overall' and country != 'overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x

def data_over_time(df,col):
    df = df[df['Season'] != 'Winter']
    nations_over_time = (
        df.drop_duplicates(['Year', 'region'])
        .groupby('Year')
        .count()['region']
        .reset_index()
        .sort_values('Year')
    )
    nations_over_time.rename(columns={'Year': "Edition", "region": "No. of Countries"}, inplace=True)
    return nations_over_time

def events_over_time(df, col):
    events_over_time = (
        df.drop_duplicates(['Year', 'Event'])
        .groupby('Year')
        .count()['Event']
        .reset_index()
        .sort_values('Year')
    )
    events_over_time.rename(columns={'Year': "Edition", "Event": "No. of Events"}, inplace=True)
    return events_over_time

def athletes_over_time(df, col):
    athletes_over_time = (
        df.drop_duplicates(['Year', 'Name'])
        .groupby('Year')
        .count()['Name']
        .reset_index()
        .sort_values('Year')
    )
    athletes_over_time.rename(columns={'Year': "Edition", "Name": "No. of Atheletes"}, inplace=True)
    return athletes_over_time


def top_athletes(medal_df, n=15):
    athlete_medals = (
        medal_df.groupby(['Name', 'region'])
        .count()['Medal']
        .reset_index()
        .sort_values('Medal', ascending=False)
        .reset_index(drop=True)
    )
    return athlete_medals.head(n)

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df