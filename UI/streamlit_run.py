import streamlit as st

login_page = st.Page(
    page="pages/login.py",
    title="Login",
    icon=":material/account_circle:",
    default=True
)
home_page = st.Page(
    page="pages/home.py",
    title="Home",
    icon=":material/account_circle:"
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

if st.user.is_logged_in:
    pg = st.navigation(pages=[home_page, plots_page, history_page], position="top")
else:
    pg = st.navigation(pages= [login_page], position="hidden")

# --- Config ---
st.set_page_config(layout="wide")
st.set_page_config(initial_sidebar_state="collapsed")
# streamlit run .\ui\streamlit_run.py
if st.sidebar.button("Log out"):
    st.logout()

pg.run()