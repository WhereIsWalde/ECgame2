import streamlit as st
from game.DatabaseManager import DatabaseManager

@st.cache_resource
def get_manager():
    # This runs exactly once when the server starts
    return DatabaseManager()

@st.cache_data(ttl=86400) # Cache for 24 hours
def get_nations_data(game_id: int):
    # We retrieve the cached manager INSIDE this function
    db = get_manager()
    return db.fetch_nations_as_pd_dataframe(game_id=game_id)

