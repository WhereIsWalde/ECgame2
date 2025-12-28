import streamlit as st
from game.DatabaseManager import DatabaseManager
from st_util import get_manager

if not st.user.is_logged_in:
    st.login("auth0")
    # st.user.sub is the unique user_id (str)

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

pg = st.navigation(pages=[home_page, plots_page, history_page], position="top")
# --- Config ---
st.set_page_config(layout="wide")
st.set_page_config(initial_sidebar_state="collapsed")

# streamlit run streamlit_run.py
if st.sidebar.button("Log out"):
    st.logout()

pg.run()