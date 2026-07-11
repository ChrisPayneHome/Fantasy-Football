import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.header("📊 Player Analytics")

@st.cache_data
def load_players():
    return pd.read_parquet("../data/current_player_data.parquet")

players = load_players()

player = st.selectbox(
    "Select Player",
    players["full_name"].unique()
)

player_df = players[players["full_name"] == player]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Price", f"£{player_df.now_cost.values[0]}")
col2.metric("Total Points", player_df.total_points.values[0])
col3.metric("Minutes", player_df.minutes.values[0])
col4.metric("Points/Cost Ratio", player_df.total_points.values[0]/player_df.now_cost.values[0])

highlight_df = players[players["full_name"] == player]
others_df = players[players["full_name"] != player]



st.subheader("Point v Cost Relationship")

fig = go.Figure()

# Other players (greyed out)
fig.add_trace(
    go.Scatter(
        x=others_df["now_cost"],
        y=others_df["total_points"],
        mode="markers",
        name="Other Players",
        marker=dict(
            color="grey",
            opacity=0.5,
            size=8
        ),
        hovertext=others_df["full_name"],
        hoverinfo="text"
    )
)

# Highlighted player
fig.add_trace(
    go.Scatter(
        x=highlight_df["now_cost"],
        y=highlight_df["total_points"],
        mode="markers",
        name=player,
        marker=dict(
            color="red",
            opacity=1.0,
            size=12
        ),
        hovertext=highlight_df["full_name"],
        hoverinfo="text"
    )
)

# Optional LOWESS trendline (computed using px)
trendline_fig = px.scatter(
    players,
    x="now_cost",
    y="total_points",
    trendline="lowess"
)

fig.add_traces(trendline_fig.data)

fig.update_layout(
    xaxis_title="Current Cost",
    yaxis_title="Current Points",
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)
