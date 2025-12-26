import streamlit as st
import pandas as pd
st.title("Nation's dashboard")
decision_col, state_col = st.columns([2,1], gap="medium", border=True)

with decision_col:
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
with state_col:
    pass