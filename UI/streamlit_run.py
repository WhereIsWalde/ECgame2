import streamlit as st
import DatabaseManager

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

#@st.cache_resource
#def get_manager():
#    # This runs exactly once when the server starts
#    return DatabaseManager()

#@st.cache_data(ttl=86400) # Cache for 24 hours
#def get_nations_data(game_id: int):
#    # We retrieve the cached manager INSIDE this function
#    db = get_manager()
#    return db.fetch_nations_as_pd_dataframe(game_id=game_id)


pg = st.navigation(pages=[home_page, plots_page, history_page], position="top")
# --- Config ---
st.set_page_config(layout="wide")
st.set_page_config(initial_sidebar_state="collapsed")

# streamlit run .\ui\streamlit_run.py
if st.sidebar.button("Log out"):
    st.logout()

pg.run()