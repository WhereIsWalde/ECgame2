import streamlit as st

login_page = st.Page(
    page="pages/login.py",
    title="Login",
    icon=":material/account_circle:"
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

pg = st.navigation(pages=[login_page, home_page, plots_page, history_page])
# --- Config ---
st.set_page_config(layout="wide")
# streamlit run .\ui\streamlit_run.py
pg.run()