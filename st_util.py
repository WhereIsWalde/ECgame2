import streamlit as st
from game.DatabaseManager import DatabaseManager

@st.cache_resource
def get_manager():
    # This runs exactly once when the server starts
    return DatabaseManager()

@st.cache_data(ttl=86400) 
def get_nations_data(game_id: int):
    # We retrieve the cached manager INSIDE this function
    db = get_manager()
    return db.fetch_nations_as_pd_dataframe(game_id=game_id)

@st.cache_data(ttl=86400) 
def get_active_game_id(user_id: str) -> int|None:
    db = get_manager()
    return db.fetch_active_game_id(user_id=user_id)

@st.cache_data(ttl=86400)
def get_current_round_id(game_id: int) -> int|None:
    db = get_manager()
    return db.fetch_current_round_id(game_id = game_id)

