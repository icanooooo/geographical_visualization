import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(layout="wide")
# st.write("""
# This is the introduction of the Project!
# """)

df = pd.read_csv('csv/votes_cleansed.csv')

votes = df.groupby(["province", "candidate_name"]).agg({
    "vote_values": "sum"
})

winners = votes.groupby(["province"])["vote_values"].idxmax()
winning_df = votes.loc[winners].reset_index()

with open("sources/id.json", "r", encoding="utf-8") as f:
    geojson_data = json.load(f)

fig = px.choropleth(
    winning_df,
    geojson=geojson_data,
    featureidkey="properties.name",
    locations="province",
    color="candidate_name",
    hover_name="province",
    hover_data=["vote_values"],
    title='Colored Map Graph 🌏'
)

fig.update_layout(width=950, height=550)
fig.update_geos(fitbounds="geojson", visible=False)
st.plotly_chart(fig, use_container_width=True)

# st.dataframe(winning_df)  