import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
data = pd.read_csv("csv/votes_cleansed.csv")

# Aggregate votes per region and candidate
vote_counts = data.groupby(["province", "candidate_name", "party_name"])["vote_values"].sum().reset_index()

# Get the winner in each province
winners = vote_counts.loc[vote_counts.groupby("province")["vote_values"].idxmax()]

# Sidebar Filters
province_filter = st.sidebar.multiselect("Select Provinces", winners["province"].unique())
if province_filter:
    winners = winners[winners["province"].isin(province_filter)]

# Display results
st.title("Voting Results by Region")
st.dataframe(winners)

# Bar Chart
fig = px.bar(winners, x="province", y="vote_values", color="candidate_name", 
             title="Winning Candidate in Each Province", labels={"vote_values": "Votes"})
st.plotly_chart(fig)
