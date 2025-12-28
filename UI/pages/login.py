import streamlit as st

if not st.user.is_logged_in:
    st.login("auth0")


# st.user.sub is the unique user_id (str)


