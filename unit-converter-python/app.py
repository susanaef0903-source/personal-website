# ============================================
# Unit converter: kilometers <-> miles
# Python + Streamlit version
#
# To run it:  streamlit run app.py
# ============================================

import streamlit as st

# 1 kilometer = 0.621371 miles — the same single fact the web version uses
MILES_PER_KM = 0.621371

st.title("Unit Converter")
st.caption("Convert between kilometers and miles")

# Streamlit builds the input controls for us — no HTML or CSS needed
amount = st.number_input("Amount", min_value=0.0, value=10.0, step=1.0)
direction = st.selectbox("Direction", ["Kilometers → Miles", "Miles → Kilometers"])

# No button required: Streamlit reruns this whole script
# every time the user changes an input, so the answer updates live
if direction == "Kilometers → Miles":
    converted = amount * MILES_PER_KM
    st.success(f"{amount:,g} km = {converted:,.4f} mi")
else:
    converted = amount / MILES_PER_KM
    st.success(f"{amount:,g} mi = {converted:,.4f} km")
