import streamlit as st
import pandas as pd
from st_util import get_nations_data, get_active_game_id, get_current_round_id
from game.tables import Nation
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt

st.title("Nation's dashboard")

def create_chart(df, column, color, chart_type, height = 150):
    chart_data = df[[column]].copy()
    if chart_type == "bar":
        st.bar_chart(chart_data, y=column, color=color, height=height)
    if chart_type == "area":
        st.area_chart(chart_data, y=column, color=color, height=height)

def display_chart(col, title, value, df, column, color):
    with st.container(border=True):
        pass
def display_speedometer_chart(current_value, min_value, max_value, text="" ):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = current_value,
        domain = {'x': [0.088, 0.912], 'y': [0, 0.9]},
        title = {
        'text': "Environment quality",
        # Explicitly set font size here
        'font': {'size': 14, 'color': "white"}  
        },
        gauge = {
            'axis': {'range': [min_value, max_value]},
            'bar': {'color': "#00A36C"},
            'steps': [
                {'range': [0, 3], 'color': "#F54927"},
                {'range': [3, 7], 'color': "gray"},
                {'range': [7, 10], 'color': "green"}
            ]
        },
        number = {
        # Explicitly set font size here
        'font': {'size': 24, 'color': "white"} 
    }
    ))
    fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    # Optional: Visualizing the background helps verify the position
    # font={'color': "white"}
)
    with st.container(border=True):
        st.plotly_chart(fig, width="stretch", height=200)


def display_pie_chart(title="", **kwargs):
    fig = px.pie(values=kwargs.values(), names=kwargs.keys(), title=title, color_discrete_sequence=["#FF5733", "#33FF57", "#3357FF"])
    fig.update_layout(
        # 1. CENTER THE TITLE
        title={
            'text': "Energy distribution",
            'y': 0.95,  # Position near the very top
            'x': 0.5,   # Center horizontally
            'xanchor': 'center',
            'yanchor': 'top'
        },
        # We keep 't' at 30 to leave just enough room for the title
        margin=dict(l=0, r=0, b=0, t=30),
        showlegend=False
    )
    fig.update_traces(
        hovertemplate='<b>%{label}</b>: %{value}<extra></extra>'
    )
    with st.container(border=True):
        st.plotly_chart(fig, width="stretch", height=200)

def get_current_data_and_deltas(nation_df: pd.DataFrame):
    numeric_cols = nation_df.select_dtypes(include=['number']).columns
    current_nation_df = nation_df[nation_df["round_id"] == st.session_state.current_round][numeric_cols].copy()
    previous_nation_df = nation_df[nation_df["round_id"] == st.session_state.current_round - 1][numeric_cols].copy()

    deltas: pd.DataFrame= current_nation_df.reset_index(drop=True)- previous_nation_df.reset_index(drop=True)
    deltas = deltas.to_dict()
    deltas: dict[str, float] = {key: np.round(ddict.get(0, 0.0), 2) for key, ddict in deltas.items()}

    data = current_nation_df.reset_index(drop=True).to_dict()
    data: dict[str, float] = {key: np.round(ddict.get(0, 0.0), 2) for key, ddict in data.items()}
    return data, deltas

all_nations_df: pd.DataFrame = get_nations_data(game_id=st.session_state.game_id)
nation_df: pd.DataFrame = all_nations_df[all_nations_df["user_id"] == st.user.sub].copy()
data, deltas = get_current_data_and_deltas(nation_df=nation_df)

#st.header("Nation")

with st.container(border=True):
    state_col1, state_col2, state_col3 = st.columns(3, gap="small", border=True)
    with state_col1:
        sub_col11, sub_col12 = st.columns(2)
        with sub_col11:
            st.metric("Total utility", value=data["total_utility"], delta=deltas["total_utility"])
            st.metric("Population", value=data["population"], delta=deltas["population"])
            st.metric("Birth rate", value=data["birth_rate"], delta=deltas["birth_rate"])
            st.metric("Death rate", value=data["death_rate"], delta=deltas["death_rate"])
            st.metric("Human services capital", value=data["human_services_capital"], delta=deltas["human_services_capital"])
        with sub_col12:
            st.metric("Effect of trade on developement", value=data["effect_of_trade_on_developement"], delta=deltas["effect_of_trade_on_developement"])
            st.metric("Wealth", value = data["wealth"], delta=deltas["wealth"])
    with state_col2:
        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            display_speedometer_chart(data["environment_quality"], 0.0, 10.0, text="Environment quality")
        with sub_col2:
            display_pie_chart(title="Energy distribution",
                               Fossil_fuel_power = data["prod_cap_fossil_fuels"],
                               Renewable_electricity = data["prod_cap_renewable_electricity"],
                               Nuclear_electricity = data["prod_cap_nuclear_electricity"]
                               )
        st.metric("Food: energy need for full capacity", value=np.ceil(Nation.elec_to_full_capacity_food(data["prod_cap_food"], data["energy_efficiency_multiplier"])))
        st.metric("Goods: energy need for full capacity", value=np.ceil(Nation.elec_to_full_capacity_goods(data["prod_cap_goods"], data["energy_efficiency_multiplier"])))
        st.metric("Population: energy need for full capacity", value=np.ceil(Nation.elec_to_full_capacity_pop(data["population"])))
        st.metric("Energy efficiency multiplier", value=data["energy_efficiency_multiplier"], delta=deltas["energy_efficiency_multiplier"])


    with state_col3:
        df_res = nation_df[nation_df["round_id"] == st.session_state.current_round][[
            "resources_LQfood", "resources_HQfood", "resources_specials", "resources_LQgoods", 
            "resources_HQgoods" , "resources_electricity", "resources_fossil_fuels"
            ]].T
        df_res.columns = ["Resources"]
        st.dataframe(df_res.round(1))

        df_prod_cap = nation_df[nation_df["round_id"] == st.session_state.current_round][[
            "prod_cap_food", "prod_cap_goods", "prod_cap_fossil_fuels", "prod_cap_renewable_electricity", 
            "prod_cap_nuclear_electricity" , "prod_cap_energy_efficiency", "prod_cap_environment", "prod_cap_human_services"
            ]].T
        df_prod_cap.columns = ["Production capital"]
        st.dataframe(df_prod_cap.round(1))



st.header("Current 5-year plan")

with st.form(key="decisions_form"):
    dec_col1, dec_col2, dec_col3 = st.columns(3, gap="small", border=True)
    with dec_col1:
        st.subheader("Area management")
        farm_area_fraction = st.slider("Farm area fraction", min_value=0.0, max_value=1.0, step = 0.01)
        production_area_fraction = st.slider("Production area fraction", min_value=0.0, max_value=1.0, step = 0.01)
        st.subheader("Food management")
        st.slider("Low quality food fraction", min_value=0.0, max_value=1.0, step = 0.01)
        st.slider("High quality food fraction", min_value=0.0, max_value=1.0, step = 0.01)
        st.slider("Specials fraction", min_value=0.0, max_value=1.0, step = 0.01)
        st.subheader("Goods management")
        st.slider("Low quality goods fraction", min_value=0.0, max_value=1.0, step = 0.01)
        st.slider("higs quality goods fraction", min_value=0.0, max_value=1.0, step = 0.01)

    with dec_col2:
        df_commerce = pd.DataFrame(0, index = ["LQfood", "HQfood", "specials", "LQgoods","HQgoods", "electricity", "fossil fuels"], columns= ["Import", "Export"])
        st.subheader("Commerce")
        st.data_editor(df_commerce)

        st.subheader("Investments")
        df_investments = pd.DataFrame(0, index=["food", "goods", "fossil fuels", "renewable_electricity", "nuclear_electricity", "energy_efficiency", "environment", "human services"], columns=["Invest"])
        st.data_editor(df_investments)
    
    with dec_col3:
        st.subheader("Electricity")
        elec_to_food = st.number_input("Electricity allocated to food", min_value=0, step=10)
        elec_to_goods = st.number_input("Electricity allocated to goods", min_value=0, step=10)
        fossil_fuels_burned = st.number_input("Fossil fuels burned", min_value=0, step=10)

        st.subheader("Resource distribution")
        df_distribution = pd.DataFrame(0, index=["LQfood", "HQfood", "specials", "LQgoods", "HQgoods"], columns=["distribute"])
        st.data_editor(df_distribution)

    st.form_submit_button("Save decisions")
