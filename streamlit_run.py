import streamlit as st
#from game.DatabaseManager import DatabaseManager
from st_util import get_active_game_id, get_current_round_id, get_manager, get_nations_data, get_market_info


if not st.user.is_logged_in:
    st.login("auth0")
    st.header("Welcome to the National Economy Game")
    st.write("Sending you to authenticate through Auth0...")
    st.stop()
    # st.user.sub is the unique user_id (str)
join_page = st.Page(
    page="pages/join.py",
    title="Join",
    icon=":material/account_circle:",
)
home_page = st.Page(
    page="pages/home.py",
    title="Home",
    icon=":material/home:",
    default=True
)
plots_page = st.Page(
    page="pages/plots.py",
    title="Plots",
    icon=":material/monitoring:"
)
history_page = st.Page(
    page="pages/history.py",
    title="History",
    icon=":material/account_circle:"
)
help_page = st.Page(
    page="pages/help.py",
    title="Help",
    icon=":material/help:"
)


if get_active_game_id(st.user.sub) == None:
    pg = st.navigation([join_page])
    st.set_page_config(layout="centered")
else:
    pg = st.navigation(pages=[home_page, plots_page, help_page], position="top")
    st.set_page_config(layout="wide")
    st.session_state["game_id"] = get_active_game_id(user_id=st.user.sub)
    st.session_state["current_round"] = get_current_round_id(st.session_state.game_id)

# --- Config ---
st.set_page_config(initial_sidebar_state="collapsed")

# streamlit run streamlit_run.py
if st.sidebar.button("Log out", type="primary"):
    st.logout()

if st.user.email == st.secrets.db.DEV_EMAIL:
    if st.sidebar.button("Advance round"):
        get_manager().advance_round(game_id=st.session_state.game_id, round_id= st.session_state.current_round)
        get_current_round_id.clear(game_id=st.session_state.game_id)
        get_nations_data.clear(game_id=st.session_state.game_id)
        get_market_info.clear(game_id=st.session_state.game_id)
        st.rerun()

pg.run()