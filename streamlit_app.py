import streamlit as st
import pandas as pd
import plotly.express as px
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

def create_proporional_bar_chart(dataframe, region):
    if region != "All":
        dataframe = dataframe[dataframe['province'] == region]

    popularity_counts = dataframe.groupby("candidate_name")['vote_values'].sum().reset_index()
    popularity_counts = popularity_counts.sort_values(by="vote_values", ascending=False)

    total_votes = popularity_counts['vote_values'].sum()
    popularity_counts["Percentage"] = (popularity_counts["vote_values"] / total_votes) * 100

    fig = px.bar(
        popularity_counts,
        x='vote_values',
        y='candidate_name',
        orientation="h",
        text='vote_values',
        color="candidate_name",
        color_discrete_sequence=px.colors.qualitative.Set3,
        title="Vote distribution by Popularity Vote"
    )

    fig.update_traces(texttemplate="%{text}", textposition='inside')
    fig.update_layout(
        xaxis_title="Number of Votes",
        yaxis_title="Candidate Name",
        showlegend=False,
        height=500
    )

    # Pakai seaborn tp masih error
    # widths = popularity_counts['Percentage']

    # # Generate a Marimekko Chart
    # fig, ax = plt.subplots(figsize=(10, 4))
    # left = 0

    # colors = plt.cm.tab10(np.linspace(0, 1, len(popularity_counts)))

    # for i, (candidate, votes, pct) in enumerate(zip(popularity_counts['candidate_name'],
    #                                                         popularity_counts['vote_values'], 
    #                                                         widths)):
    #     ax.barh(["Votes"], [pct], left=left, color=colors[i], label=f"{candidate}")
    #     ax.text(left + pct / 2, 0, f"{votes}\n({pct:.1%})", ha="center", va="center", fontsize=10, color="white", weight="bold")
    #     left += pct

    # ax.set_xticks([])
    # ax.set_yticks([])
    # ax.set_frame_on(False)
    # ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
    
    return fig

st.set_page_config(layout="wide")

df = pd.read_csv('csv/votes_cleansed.csv')

votes = df.groupby(["province", "candidate_name"]).agg({
    "vote_values": "sum"
})

winners = votes.groupby(["province"])["vote_values"].idxmax()
winning_df = votes.loc[winners].reset_index()

col = st.columns((6, 3), gap='medium')

with st.sidebar:
    regions = ["All", "DKI Jakarta"]
    selected_region = st.selectbox("Select Region", regions )

with col[0]:
    a = make_choropleth(winning_df, "province", "candidate_name")

    st.plotly_chart(a, use_container_width=True)

    col_col = st.columns((5,5), gap='small')

    with col_col[0]:
        popularity_fig = create_proporional_bar_chart(df, selected_region)

        st.plotly_chart(popularity_fig)
    with col_col[1]:
        st.write("i want to learn rust")

with col[1]:
    st.dataframe(winning_df)

# st.dataframe(winning_df)  