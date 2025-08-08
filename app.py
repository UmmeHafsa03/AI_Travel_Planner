import streamlit as st
from dotenv import load_dotenv
from src.core.planner import TravelPlanner

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="🌍 AI Travel Planner", layout="wide")

# -------------------- CUSTOM CSS STYLING --------------------
st.markdown("""
    <style>
        .stApp {
            background-color: black;
            font-family: 'Segoe UI', sans-serif;
        }
        .title-style {
            font-size: 40px;
            font-weight: bold;
            color: #00bfff;
            text-align: center;
            margin-top: 30px;
        }
        .subtitle-style {
            font-size: 20px;
            color: white;
            text-align: center;
            margin-bottom: 40px;
        }
        .stTextInput > label, .stNumberInput > label {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- PAGE TITLE --------------------
st.markdown("<h1 class='title-style'>🧳 AI Travel Itinerary Planner</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-style'>Plan your dream trip in seconds by entering your city, interests and number of days ✨</p>", unsafe_allow_html=True)

# -------------------- ENV VARIABLES --------------------
load_dotenv()

# -------------------- MAIN FORM --------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    with st.form("planner_form"):
        city = st.text_input("📍 Enter the city name for your trip")
        days = st.number_input("🗓️ Number of days for your trip", min_value=1, max_value=30, value=3)
        interests = st.text_input("💡 Your interests (comma-separated)", placeholder="Food, Nature, Culture")
        submitted = st.form_submit_button("🚀 Generate Itinerary")

        if submitted:
            if city and interests and days:
                with st.spinner("✨ Generating your itinerary... hang tight!"):
                    planner = TravelPlanner()
                    planner.set_city(city)
                    planner.set_interests(interests)
                    planner.set_days(days)
                    itinerary = planner.create_itineary()

                st.success("🎉 Here's your personalized travel itinerary!")
                st.markdown("### 🗓️ Day-wise Plan")

                # ✅ Display the AI-generated itinerary without duplicating "Day 1"
                days_split = itinerary.split("\n\n")
                for day in days_split:
                    st.markdown(day)
                    st.markdown("---")

            else:
                st.warning("⚠️ Please fill in all the fields to continue.")
