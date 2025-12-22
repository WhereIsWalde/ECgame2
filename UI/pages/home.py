import streamlit as st
st.title("Nation's dashboard")
decision_col, state_col = st.columns([2,1], gap="medium", border=True)

with decision_col:
    st.header("Current 5-year plan")
    
    with st.form(key="decisions_form"):
        dec_col1, dec_col2, dec_col3 = st.columns(3, gap="small", border=True)
        with dec_col1:
            farm_area_fraction = st.slider("Farm area fraction", min_value=0.0, max_value=1.0, step = 0.01)
            production_area_fraction = st.slider("Production area fraction", min_value=0.0, max_value=1.0, step = 0.01)
            st.divider()
            st.slider("Low quality food fraction", min_value=0.0, max_value=1.0, step = 0.01)
            st.slider("High quality food fraction", min_value=0.0, max_value=1.0, step = 0.01)
            st.slider("Specials fraction", min_value=0.0, max_value=1.0, step = 0.01)
            st.divider()
            st.slider("Low quality goods fraction", min_value=0.0, max_value=1.0, step = 0.01)
            st.slider("higs quality goods fraction", min_value=0.0, max_value=1.0, step = 0.01)

        st.form_submit_button("Save decisions")
with state_col:
    pass