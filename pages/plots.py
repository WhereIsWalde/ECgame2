import streamlit as st
import pandas as pd
from st_util import get_market_info, get_nations_data
import altair as alt

def display_multi_line_chart(df, x:str, y:str, x_label:str, y_label:str, color:str):
    nearest = alt.selection_point(
        nearest=True, 
        on='mouseover', 
        empty=False
    )
    base = alt.Chart(df).encode(
        x=alt.X(f"{x}:Q", title=x_label),
        y=alt.Y(f"{y}:Q", title=y_label),
        color=alt.Color(f"{color}:N", legend=None)
    )
    lines = base.mark_line()
    points = base.mark_point().encode(
        opacity=alt.value(0),  
        tooltip=[x, color, y]  # The tooltip appears when the invisible point is "snapped"
    ).add_params(nearest)
    chart = alt.layer(lines, points).interactive().properties(
        width='container', 
        height=350
    )
    st.altair_chart(chart, width="stretch")

market_info: pd.DataFrame = get_market_info(game_id = st.session_state.game_id)
nations_info: pd.DataFrame = get_nations_data(game_id = st.session_state.game_id)

st.title("State of the game")

state_tab, price_tab= st.tabs(["Game State", "Prices"])

with state_tab:
    col9, col10, col11, col12 = st.columns(4)

    with col9:
        st.markdown("#### Total utility")
        #st.line_chart(nations_info, x = "round_id", y = "total_utility", color="nation_name", x_label="Round", y_label="Utility")
        display_multi_line_chart(nations_info, x = "round_id", y = "total_utility", x_label="Round", y_label="Utility", color="nation_name")

    with col10:
        st.markdown("#### Tons of goods manufactured")
        display_multi_line_chart(nations_info, x = "round_id", y = "prod_cap_goods", x_label="Round", y_label="Goods", color="nation_name")

    with col11:
        st.markdown("#### Tons of food manufactured")
        display_multi_line_chart(nations_info, x = "round_id", y = "prod_cap_food", x_label="Round", y_label="Food", color="nation_name")

    with col12:
        st.markdown("#### Population")
        display_multi_line_chart(nations_info, x = "round_id", y = "population", x_label="Round", y_label="Population", color="nation_name")

    st.divider()
    col13, col14, col15, col16 = st.columns(4)

    with col13:
        st.markdown("#### Trading profiency")
        display_multi_line_chart(nations_info, x = "round_id", y = "effect_of_trade_on_developement", x_label="Round", y_label="ETD", color="nation_name")

    with col14:
        st.markdown("#### Financial affairs")
        display_multi_line_chart(nations_info, x = "round_id", y = "wealth", x_label="Round", y_label="Wealth", color="nation_name")

    with col15:
        st.markdown("#### Education level")
        display_multi_line_chart(nations_info, x = "round_id", y = "human_services_capital", x_label="Round", y_label="HSC", color="nation_name")

    with col16:
        st.markdown("#### Environmental protection")
        display_multi_line_chart(nations_info, x = "round_id", y = "prod_cap_environment", x_label="Round", y_label="Environment investment", color="nation_name")

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
        