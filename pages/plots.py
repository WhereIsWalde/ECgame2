import streamlit as st
import pandas as pd
from st_util import get_market_info

market_info: pd.DataFrame = get_market_info(game_id = st.session_state.game_id)

st.title("State of the game")

price_tab, tab2, tab3 = st.tabs(["Prices", "Supply", "Demand"])

with price_tab:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("#### Price of low quality food")
        st.line_chart(market_info["price_LQfood"], x_label="Round", y_label="Price")

    with col2:
        st.markdown("#### Price of high quality food")
        st.line_chart(market_info["price_HQfood"], x_label="Round")

    with col3:
        st.markdown("#### Price of specials")
        st.line_chart(market_info["price_specials"], x_label="Round")

    with col4:
        st.markdown("#### Price of low quality goods")
        st.line_chart(market_info["price_LQgoods"], x_label="Round")

    st.divider()
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.markdown("#### Price of high quality goods")
        st.line_chart(market_info["price_HQgoods"], x_label="Round", y_label="Price")

    with col6:
        st.markdown("#### Price of electricity")
        st.line_chart(market_info["price_electricity"], x_label="Round")

    with col7:
        st.markdown("#### Price of fossil fuels")
        st.line_chart(market_info["price_fossil_fuels"], x_label="Round")

    with col8:
        st.markdown("#### Price comparison")
        st.line_chart(market_info[["price_LQfood", "price_HQfood", "price_specials", "price_LQgoods", "price_HQgoods", "price_electricity", "price_fossil_fuels"]], 
                       x_label="Round")