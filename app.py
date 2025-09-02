import re
import streamlit as st
from dotenv import load_dotenv
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from src.core.planner import TravelPlanner
import random

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="🌍 AI Travel Planner", layout="wide")

# -------------------- LIGHT CSS --------------------
st.markdown("""
    <style>
        .stApp {
            background: url("https://t4.ftcdn.net/jpg/03/36/45/65/360_F_336456579_K00FCLKIIbG6vtiWbnbqVcUuvVv35GSF.jpg") no-repeat center center fixed;
            background-size: cover;
            font-family: 'Poppins', sans-serif;
            color: white;
        }
        .stApp:before {
            content: "";
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0,0,0,0.6);
            z-index: -1;
        }
        .title-style {
            font-size: 42px;
            font-weight: bold;
            text-align: center;
            color: #FFD700;
            margin-top: 15px;
            text-shadow: 2px 2px 5px #000;
        }
        .subtitle-style {
            font-size: 20px;
            text-align: center;
            color: #f0f0f0;
            margin-bottom: 25px;
        }
        .day-card {
            background: white;
            padding: 18px;
            border-radius: 12px;
            margin-bottom: 15px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.3);
            color: black;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.markdown("<h1 class='title-style'>🧳 AI Travel Itinerary Planner</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-style'>Plan your dream trip in seconds ✨</p>", unsafe_allow_html=True)

# -------------------- ENV VARIABLES --------------------
load_dotenv()

# -------------------- SESSION STORAGE --------------------
if "history" not in st.session_state:
    st.session_state["history"] = []

# -------------------- PDF GENERATORS --------------------
def create_pdf_single(entry):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"<b>{entry['City']} ({entry['Days']} days)</b>", styles["Title"]))
    story.append(Paragraph(f"Interests: {entry['Interests']}", styles["Normal"]))
    story.append(Paragraph(entry['Itinerary'].replace("\n", "<br/>"), styles["Normal"]))
    story.append(Spacer(1, 12))

    doc.build(story)
    buffer.seek(0)
    return buffer

def create_checklist_pdf(city):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"<b>Travel Checklist for {city}</b>", styles["Title"]))
    checklist_items = [
        "Passport/ID",
        "Travel tickets / Boarding passes",
        "Hotel reservation confirmations",
        "Local currency / Credit cards",
        "Phone, charger & power bank",
        "Medications & first-aid kit",
        "Clothing appropriate for destination",
        "Toiletries",
        "Camera / Gadgets",
        "Sunglasses / Hat / Sunblock",
        "Travel guide / Map",
        "Snacks / Water bottle"
    ]
    for item in checklist_items:
        story.append(Paragraph(f"- {item}", styles["Normal"]))
    story.append(Spacer(1, 12))

    doc.build(story)
    buffer.seek(0)
    return buffer

# -------------------- SIDEBAR --------------------
st.sidebar.header("📜 Saved Itineraries")
if st.session_state["history"]:
    for i, entry in enumerate(st.session_state["history"], 1):
        st.sidebar.markdown(f"{i}. {entry['City']} ({entry['Days']} days) — {entry['Interests']}")

    # Get the latest itinerary
    latest_itinerary = st.session_state["history"][-1]

    # Download buttons with emojis
    st.sidebar.download_button(
        "📥 📄 Download Latest Itinerary (PDF)",
        create_pdf_single(latest_itinerary),
        f"{latest_itinerary['City']}_Itinerary.pdf",
        "application/pdf"
    )
    st.sidebar.download_button(
        "📥 📝 Download Travel Checklist (PDF)",
        create_checklist_pdf(latest_itinerary["City"]),
        f"{latest_itinerary['City']}_Checklist.pdf",
        "application/pdf"
    )
else:
    st.sidebar.info("📜 Saved itineraries or history will appear here after generating your first trip!")


# -------------------- BUDGET ESTIMATOR --------------------
def estimate_budget(days):
    hotel_per_day = random.randint(4000, 15000)
    food_per_day = random.randint(800, 2500)
    travel_per_day = random.randint(500, 2000)
    total = (hotel_per_day + food_per_day + travel_per_day) * days
    breakdown = f"""
Estimated Budget (INR)  

- 🏨 Hotel: ₹{hotel_per_day} x {days} days = ₹{hotel_per_day*days}  
- 🍽 Food: ₹{food_per_day} x {days} days = ₹{food_per_day*days}  
- 🚗 Travel: ₹{travel_per_day} x {days} days = ₹{travel_per_day*days}  

Total ≈ ₹{total}
"""
    return breakdown

# -------------------- FORM --------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    with st.form("planner_form_unique"):
        city = st.text_input("📍 Enter the city name")
        days = st.number_input("🗓 Number of days", min_value=1, max_value=30, value=3)
        interests = st.text_input("💡 Your interests", placeholder="Food, Nature, Culture")
        submitted = st.form_submit_button("🚀 Generate Itinerary")

        if submitted:
            if city and interests and days:
                with st.spinner("✨ Crafting your itinerary..."):
                    try:
                        planner = TravelPlanner()
                        planner.set_city(city)
                        planner.set_interests(interests)
                        planner.set_days(days)
                        itinerary = planner.create_itineary()
                    except Exception:
                        itinerary = f"""
                        Day 1: Arrival at {city}, evening city walk.  
                        Day 2: Explore cultural spots + try local food.  
                        Day 3: Relax, shopping & farewell dinner.  
                        """

                st.success("🎉 Your personalized travel itinerary is ready!")

                st.session_state["history"].append({
                    "City": city, "Days": days, "Interests": interests, "Itinerary": itinerary
                })

                # Display itinerary
                days_split = re.split(r'(?=\*\*Day\s+\d+)', itinerary.strip())
                for day in days_split:
                    if not day.strip(): continue
                    day_html = day.replace("\n", "<br>")
                    st.markdown(f"<div class='day-card'>{day_html}</div>", unsafe_allow_html=True)

                # Budget
                budget_text = estimate_budget(days)
                st.info(budget_text)

            else:
                st.warning("⚠ Please fill all fields to continue.")

# -------------------- IMAGE UPLOAD --------------------
st.subheader("📸 Upload Your Travel Images")
uploaded_files = st.file_uploader("Upload images", accept_multiple_files=True, type=["png","jpg","jpeg"])
if uploaded_files:
    for file in uploaded_files:
        st.image(file, caption=file.name, use_container_width=True)