import streamlit as st
from pint import UnitRegistry  # Unit conversion
import openai  # AI-powered explanations
import matplotlib.pyplot as plt  # Graphs

# Initialize Pint UnitRegistry
ureg = UnitRegistry()
Q_ = ureg.Quantity

# OpenAI API Key (Add your own key)
openai.api_key = "your-api-key-here"

# Conversion history
conversion_history = []

def convert_units(value, from_unit, to_unit):
    try:
        quantity = Q_(value, from_unit)
        converted_quantity = quantity.to(to_unit)
        return converted_quantity.magnitude
    except:
        return None

def get_ai_explanation(unit):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Explain the unit '{unit}' in simple words."}]
        )
        return response["choices"][0]["message"]["content"]
    except:
        return "AI explanation not available."

# Streamlit App
st.set_page_config(page_title="AI-Powered Unit Converter", layout="wide")
st.title("🚀 AI-Powered Unit Converter")
st.markdown("Convert units with AI-powered explanations and live graphs!")

# Define supported units
unit_categories = {
    "Length": ["meter", "foot", "inch", "mile", "kilometer", "light_year"],
    "Mass": ["kilogram", "gram", "pound", "ounce", "ton"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
    "Volume": ["liter", "gallon", "cubic_meter", "cubic_inch"],
    "Speed": ["meter_per_second", "kilometer_per_hour", "mile_per_hour"],
    "Energy": ["joule", "calorie", "btu", "electron_volt"],
}

# UI layout
col1, col2, col3 = st.columns(3)

with col1:
    value = st.number_input("Enter value:", value=1.0, step=0.1)
with col2:
    category = st.selectbox("Select unit category:", list(unit_categories.keys()))
with col3:
    from_unit = st.selectbox("Select from unit:", unit_categories.get(category, []))

target_unit = st.selectbox("Select target unit:", unit_categories.get(category, []))

if st.button("Convert"):
    result = convert_units(value, from_unit, target_unit)
    if result is not None:
        conversion_history.append((value, from_unit, result, target_unit))
        if len(conversion_history) > 5:
            conversion_history.pop(0)
        st.success(f"✅ {value} {from_unit} = {result:.4f} {target_unit}")
        explanation = get_ai_explanation(target_unit)
        st.info(f"🤖 AI says: {explanation}")
    else:
        st.error("❌ Invalid conversion. Please check your units.")

# Display conversion history
st.subheader("📜 Conversion History")
for item in conversion_history:
    st.write(f"{item[0]} {item[1]} ➡️ {item[2]:.4f} {item[3]}")

# Graph visualization
if len(conversion_history) > 1:
    st.subheader("📊 Conversion Trends")
    fig, ax = plt.subplots()
    values = [x[2] for x in conversion_history]
    labels = [f"{x[0]} {x[1]} → {x[3]}" for x in conversion_history]
    ax.plot(labels, values, marker='o', linestyle='-', color='green')
    plt.xticks(rotation=45)
    plt.ylabel("Converted Values")
    st.pyplot(fig)

# Dark Mode Toggle
import streamlit as st

# Initialize dark mode state in session_state if not already set
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Button to toggle dark mode
if st.button("🌙 Toggle Dark Mode"):
    st.session_state.dark_mode = not st.session_state.dark_mode

# Apply CSS based on dark mode state
if st.session_state.dark_mode:
    st.markdown(
        """
        <style>
        body, .stApp {
            background-color: #121212;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        body, .stApp {
            background-color: white;
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

st.write("Dark mode is now", "enabled" if st.session_state.dark_mode else "disabled")

