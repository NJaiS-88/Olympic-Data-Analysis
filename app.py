import streamlit as st
import pandas as pd
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
st.set_page_config(layout="wide")
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)
df = df[df['Season']!='Winter']
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis')
)
if(user_menu == 'Medal Tally'):
    st.sidebar.header("Medal Tally")
    st.header("Medal Tally")
    years,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year: ", years)
    selected_country = st.sidebar.selectbox("Select Country: ", country)
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)
    nations_over_time = helper.data_over_time(df, 'region')
    fig, ax = plt.subplots()
    ax.plot(
        nations_over_time['Edition'],
        nations_over_time['No. of Countries'],
        marker="o"
    )

    ax.set_xlabel("Edition")
    ax.set_ylabel("Number of Countries")
    ax.set_title("Nations Participating Over Time")

    # Show the plot in Streamlit
    st.pyplot(fig)

    events_over_time = helper.events_over_time(df, 'Event')
    fig, ax = plt.subplots()
    ax.plot(
        events_over_time['Edition'],
        events_over_time['No. of Events'],
        marker="o"
    )

    ax.set_xlabel("Edition")
    ax.set_ylabel("Number of Events")
    ax.set_title("Number of Events Over Time")
    st.pyplot(fig)

    athletes_over_time = helper.athletes_over_time(df, 'Name')
    fig, ax = plt.subplots()
    ax.plot(
        athletes_over_time['Edition'],
        athletes_over_time['No. of Atheletes'],
        marker="o"
    )

    ax.set_xlabel("Edition")
    ax.set_ylabel("Number of Events")
    ax.set_title("Number of Athletes Over Time")
    st.pyplot(fig)

    st.title("No. of Events over time(Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.pyplot(fig)

    sports_list = sorted(df['Sport'].unique().tolist())
    sports_list.insert(0, 'overall')
    selected_sport = st.sidebar.selectbox("Select Sport", sports_list)

    # Filter by sport or overall
    if selected_sport == 'overall':
        medal_df = df.dropna(subset=['Medal'])
    else:
        medal_df = df[(df['Sport'] == selected_sport) & df['Medal'].notna()]
    top15 = helper.top_athletes(medal_df, 15)

    st.subheader(f"Top 15 Athletes in {selected_sport.title()}")
    st.table(top15)


if user_menu == 'Country-wise Analysis':
    st.header("Country-wise Analysis")

    # Sidebar country selector
    countries = sorted(df['region'].dropna().unique().tolist())
    selected_country = st.sidebar.selectbox("Select Country", countries)

    # Year-wise medal tally
    yearwise = helper.yearwise_medal_tally(df, selected_country)
    st.subheader(f"Year-wise Medal Tally for {selected_country}")
    st.table(yearwise)

    # Overall medal tally
    overall = yearwise['Medal'].sum()
    st.subheader(f"Overall Medal Tally for {selected_country}")
    st.write(f"{selected_country} has won a total of **{overall} medals**.")

    # 📊 Line chart for year-wise medals
    fig, ax = plt.subplots()
    ax.plot(yearwise['Year'], yearwise['Medal'], marker="o", linestyle="-", color="blue")
    ax.set_xlabel("Year")
    ax.set_ylabel("Medals")
    ax.set_title(f"Medals Won by {selected_country} Over Time")
    st.pyplot(fig)