import streamlit as st

st.set_page_config(
    page_title="FPL Analytics",
    layout="wide",
    page_icon="⚽"
)

st.title("⚽ Fantasy Premier League Analytics")

st.markdown("""
Welcome to your Fantasy Premier League analytics dashboard.

Use the sidebar to explore:
- Player performance
- Fixture difficulty
- Transfer optimization
""")

st.info("Data source: FPL API / custom datasets")
