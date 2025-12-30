import streamlit as st
from st_util import get_manager, get_active_game_id
import time

st.header("Welcome to the National Economy Game!")
# #FFF8DC

with st.container(border=True):
    st.markdown(
    """
    <div style="font-family: 'Courier New', Courier, monospace; color: #E9DCC9;">
        Your country is in a very bad position. Previous governments have not put an
        effort into improving and developing the country. It is up to you to solve the
        problems that your country is facing and finally improve the living standard
        of the poor citizens to match that of the developed western democracies.
    </div>
    """, 
    unsafe_allow_html=True
)

with st.form(key="join_game_form"):
    game_id = st.text_input("Game-ID")
    nation_name = st.text_input("Name of your glorious nation")
    leader_name = st.text_input("Name of your glorious leader")
    if st.form_submit_button("Join game"):
        if not game_id or not nation_name or not leader_name:
            st.error("The records are incomplete, Leader! Please fill all fields.")
        else:
            manager = get_manager()
            manager.add_new_player(user_id=st.user.sub, game_id=int(game_id), leader_name=leader_name, nation_name=nation_name)
            get_active_game_id.clear(st.user.sub)
            st.success(f"Welcome, Leader {leader_name}! Your nation of {nation_name} has been established.")
            time.sleep(3) 
            st.rerun()