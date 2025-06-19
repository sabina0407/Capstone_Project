import streamlit as st
import pandas as pd
import plotly.express as px

# Load cleaned data
df = pd.read_csv("leaders_for_wins_cleaned.csv")

# This is dashboard title and brief description 
st.title("MLB Leaderboard Dashboard")
st.markdown("Explore a year-by-year leaderboard in Major League games won for every season since 1901.")

# ==========================================
# Dropdown - Barchart of top leaders by Year
st.subheader("Top Leaders by Year")
year = st.selectbox("Select a Year", sorted(df["Year"].unique())) # Dropdown to select year
top_year = df[df["Year"] == year].sort_values(by="Wins", ascending=False) # filters data to include only the selected year

# Creates barchart and displays it 
fig1 = px.bar(top_year, x="Player", y="Wins", color="League", title=f"Top Pitchers in {year}")
st.plotly_chart(fig1)

# ==================================================================================
# Multiselect(to choose one or both leagues) - Line chart of wins over time by League
st.subheader("Wins Over Time by League")
leagues = st.multiselect("Select League(s)", df["League"].unique(), default=list(df["League"].unique()))
filtered = df[df["League"].isin(leagues)] # Filters data to include only the selected leagues 

# Creates line chart and displays it
fig2 = px.line(filtered, x="Year", y="Wins", color="League", markers=True, title="Pitching Wins Over Time")
st.plotly_chart(fig2)

# ================================================================
# Slider (to select a year range) - histogram of Wins Distribution
st.subheader("Wins Distribution")
year_range = st.slider("Select Year Range", int(df["Year"].min()), int(df["Year"].max()), (2000, 2025))
range_df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

fig3 = px.histogram(range_df, x="Wins", nbins=20, color="League", title=f"Wins Distribution ({year_range[0]}–{year_range[1]})")
st.plotly_chart(fig3)

#===================================
# Bar chart of team Leader Frequency
st.subheader("Most Frequent Leader Teams")
# count how many times each team appers as a leader
top_teams = df["Team"].value_counts().reset_index()
top_teams.columns = ["Team", "Count"]

fig4 = px.bar(top_teams.head(10), x="Team", y="Count", color="Team", title="Top 10 Leader Teams")
st.plotly_chart(fig4)

# Footer with data source
st.markdown("---")
st.caption("Data Source: Baseball Almanac - Year By Year Leaders For Wins")
