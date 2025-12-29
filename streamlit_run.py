import streamlit as st
from game.DatabaseManager import DatabaseManager
from st_util import get_active_game_id, get_current_round_id

if not st.user.is_logged_in:
    st.login("auth0")
    # st.user.sub is the unique user_id (str)

join_page = st.Page(
    page="pages/join.py",
    title="Join",
    icon=":material/account_circle:",
)
home_page = st.Page(
    page="pages/home.py",
    title="Home",
    icon=":material/account_circle:",
    default=True
)
plots_page = st.Page(
    page="pages/plots.py",
    title="Plots",
    icon=":material/account_circle:"
)
history_page = st.Page(
    page="pages/history.py",
    title="History",
    icon=":material/account_circle:"
)


if get_active_game_id(st.user.sub) == None:
    pg = st.navigation([join_page])
    st.set_page_config(layout="centered")
else:
    pg = st.navigation(pages=[home_page, plots_page, history_page], position="top")
    st.set_page_config(layout="wide")
    st.session_state["game_id"] = get_active_game_id(user_id=st.user.sub)
    st.session_state["current_round"] = get_current_round_id(st.session_state.game_id)

# --- Config ---
st.set_page_config(initial_sidebar_state="collapsed")

# streamlit run streamlit_run.py
if st.sidebar.button("Log out"):
    st.logout()

pg.run()