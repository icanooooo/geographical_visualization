import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import json

def make_choropleth(input_df, input_id, input_column):
    with open("sources/id.json", "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    fig = px.choropleth(
        input_df,
        geojson=geojson_data,
        featureidkey="properties.name",
        locations=input_id,
        color=input_column,
        hover_name=input_id,
        hover_data=["vote_values"],
        title='Colored Map Graph 🌏'
    )

    fig.update_layout(width=950, height=550)
    fig.update_geos(fitbounds="geojson", visible=False)

    return fig

def create_proporional_bar_chart(dataframe, region, column):
    if region != "All":
        dataframe = dataframe[dataframe['province'] == region]

    popularity_counts = dataframe.groupby(column)['vote_values'].sum().reset_index()
    popularity_counts = popularity_counts.sort_values(by="vote_values", ascending=False)

    total_votes = popularity_counts['vote_values'].sum()
    popularity_counts["percentage"] = (popularity_counts["vote_values"] / total_votes) * 100

    fig = go.Figure()

    left = 0

    for _, row in popularity_counts.iterrows():
        fig.add_trace(go.Bar(
            x=[row['percentage']],
            y=[1],
            text=f"{row[column]}<br>{row['vote_values']} votes<br>{row['percentage']:.1%}",
            textposition="inside",
            name=row[column],
            orientation="h"
        ))
        left += row['percentage']

    fig.update_layout(
        title="Vote Distribution by Popularity Vote",
        barmode="stack",
        showlegend=False,
        height=400
    )

    return fig

st.set_page_config(layout="wide")

df = pd.read_csv('csv/votes_cleansed.csv')

votes = df.groupby(["province", "candidate_name"]).agg({
    "vote_values": "sum"
})

winners = votes.groupby(["province"])["vote_values"].idxmax()
winning_df = votes.loc[winners].reset_index()

col = st.columns((7, 3), gap='medium')

with st.sidebar:
    regions = ["All", "DKI Jakarta"]
    selected_region = st.selectbox("Select Region", regions )

with col[0]:
    a = make_choropleth(winning_df, "province", "candidate_name")

    st.plotly_chart(a, use_container_width=True)

    col_col = st.columns((5,5), gap='small')

    with col_col[0]:
        popularity_fig = create_proporional_bar_chart(df, selected_region, 'candidate_name')

        st.plotly_chart(popularity_fig)
    with col_col[1]:
        gender_fig = create_proporional_bar_chart(df, selected_region, 'gender')

        st.plotly_chart(gender_fig)

with col[1]:
    st.dataframe(df)

# st.dataframe(winning_df)  