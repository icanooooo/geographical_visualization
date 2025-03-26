import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

def get_winning_df(df):
    votes = df.groupby(["province", "candidate_name"]).agg({
        "vote_values": "sum"
    })

    winners = votes.groupby(["province"])["vote_values"].idxmax()
    winning_df = votes.loc[winners].reset_index()

    return winning_df

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
        hover_data=["vote_values"]
    )

    fig.update_layout(width=950,
                      height=450,
                      margin=dict(l=0, r=0,t=0, b=0),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                    #   title=dict(
                    #       text='Colored Map Graph 🌏',
                    #       x=0.02,
                    #       y=0.93,
                    #       font=dict(size=20)
                    #   )
                      )
    fig.update_geos(fitbounds="geojson", visible=False)

    return fig

def create_proporional_bar_chart(dataframe, region, candidate, column, title):
    if region != "All":
        dataframe = dataframe[dataframe['province'] == region]
    if candidate != "All":
        dataframe = dataframe[dataframe['candidate_name'] == candidate]

    popularity_counts = dataframe.groupby(column)['vote_values'].sum().reset_index()
    popularity_counts = popularity_counts.sort_values(by="vote_values", ascending=False)

    total_votes = popularity_counts['vote_values'].sum()
    popularity_counts["percentage"] = (popularity_counts["vote_values"] / total_votes)

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
        title=title,
        barmode="stack",
        showlegend=False,
        height=200,
        margin=dict(l=5, r=5,t=30, b=5)
    )

    return fig

def show_winners(dataframe, winning_df, region, candidate):
    if region == 'All':
        dataframe = winning_df.groupby('candidate_name').agg({
            'province':'count'
        })
        label = 'Winner by Electoral'
        dataframe.reset_index()
        row = dataframe.loc[dataframe['province'].idxmax()]
        values = row.name
        delta = row.to_string(index=False) + " Provinces"

    else:
        dataframe = dataframe[dataframe['province'] == region]
        dataframe = dataframe.groupby('candidate_name').agg({
            'vote_values':'count'
        })
        label = f'Winner by Popular Vote on {region}'
        row = dataframe.loc[dataframe['vote_values'].idxmax()]
        values = row.name
        delta = row.to_string(index=False) + " Votes"

    return label, values, delta

def get_winner(dataframe, region):
    if region == "All":
        dataframe = get_winning_df(dataframe)

        winners_summary_df = dataframe.groupby('candidate_name').agg({
            'province':'count'
        })

        winners_summary_df = winners_summary_df.sort_values('province', ascending=False)

        winners_text = '**Electoral Votes**'

        column = 'province'
        column_name = "Total Province Won"
    else:
        winners_text = f"**Total Votes in {region}**"

        winners_summary_df = dataframe.groupby('candidate_name').agg({
            'vote_values':'count'
        })

        winners_summary_df = winners_summary_df.sort_values('vote_values', ascending=False)
        
        column = 'vote_values'
        column_name = "Total Votes in Province"

    return winners_text, winners_summary_df, column, column_name

def get_winner_dataframe(dataframe, column, column_name):
    if column == 'vote_values':
        maximum = max(dataframe.vote_values)
    else:
        maximum = max(dataframe.province)

    df = st.dataframe(dataframe,
                    column_order=('candidate_name', column),
                    column_config={
                        "candidate_name": st.column_config.TextColumn(
                            "Candidate Name",
                        ),
                        column: st.column_config.ProgressColumn(
                            column_name,
                            format="%f",
                            min_value=0,
                            max_value=maximum
                        )
                    }
                    )
    
    return df

def main():
    st.set_page_config(
        layout="wide",
        page_title= "Indonesia Political Dashboard Simulation",
        page_icon="🌏",
        initial_sidebar_state="expanded"
        )

    df = pd.read_csv('csv/votes_cleansed.csv')

    winning_df = get_winning_df(df)

    # st.title("Political Dashboard Visualization Simulation 🌏")

    col = st.columns((7, 3), gap='medium')

    with st.sidebar:
        st.title("Indonesia Political Dashboard Simulation")
        st.write("**Filters:**")

        regions = ["All"] + sorted(df["province"].unique().tolist())
        selected_region = st.selectbox("Select Province", regions )

        candidates = ["All"] + sorted(df["candidate_name"].unique().tolist())
        selected_candidate = st.selectbox("Select Candidate", candidates)

    with col[0]:
        st.markdown("## Geographical Voting Visualization 🌏")

        a = make_choropleth(winning_df, "province", "candidate_name")

        st.plotly_chart(a, use_container_width=True)

        col_col = st.columns((5,5), gap='small')

        with col_col[0]:
            popularity_fig = create_proporional_bar_chart(df, selected_region, selected_candidate, 'candidate_name', "Vote Distribution by Popularity Vote 📈")

            st.plotly_chart(popularity_fig)
        with col_col[1]:
            sex_fig = create_proporional_bar_chart(df, selected_region, selected_candidate, 'sex', "Vote Distribution by Sex ♂️♀️")

            st.plotly_chart(sex_fig)

    with col[1]:
        st.markdown("""
            <style>
                .spacer {
                    padding-top: 30px;  /* Adjust as needed */
                }
            </style>
            <div class="spacer"></div>
            <style>
            div[data-testid="stMetric"] {
                background-color: #f7f7f7;
                border-radius: 10px;
                padding: 10px;
            }
            </style>
        """, unsafe_allow_html=True)
        
        with st.expander("About", expanded=True):
            st.write('''
                ### Political Dashboard Simulation 📊:
                This project is using a generated random data using Random APIs. This dashboard by no means represent actual reality, all data shown is for simulation purposes to showcase dashboard development.
                ''')
            
        label, value, delta = show_winners(df, winning_df, selected_region, selected_candidate)
        st.metric(label=label, value=value, delta=delta)

        winners_text, winners_summary_df, column, column_name = get_winner(df, selected_region)       
        
        st.write(winners_text)
        
        get_winner_dataframe(winners_summary_df, column, column_name)

if __name__ == "__main__":
    main()  