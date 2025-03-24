import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Google Sheets Setup ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gspread_service_account"], scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open("Audi Car Recommender User Data").sheet1  # First sheet

# --- Audi Car Data ---
audi_cars = {
    "Q8": 107, "Q8 e-tron": 114, "e-tron GT": 172,
    "A4": 45.34, "A5": 60.00, "A6": 64.00,
    "Q3": 42.77, "Q5": 65.18
}

# --- Streamlit UI ---
st.title("🚗 Audi Car Recommender")
st.write("Find the best Audi car within your budget!")

# --- User Inputs ---
name = st.text_input("Enter your name:")
email = st.text_input("Enter your email:")

# Budget Slider
budget = st.slider("Select Your Budget (in Lakhs)", min_value=40, max_value=200, step=5)
st.markdown(f"<h3 style='color:green;'>Your Budget: ₹{budget} Lakhs</h3>", unsafe_allow_html=True)

# --- Recommendation Logic ---
if st.button("Get Recommendations"):
    if name and email:
        recommended_cars = [car for car, price in audi_cars.items() if price <= budget]
        if recommended_cars:
            st.success(f"🚘 Based on your budget ({budget}L), you can buy: {', '.join(recommended_cars)}")
        else:
            st.warning("⚠️ No cars match your budget. Consider increasing it.")

        # Store User Data in Google Sheets
        sheet.append_row([name, email, budget, ", ".join(recommended_cars)])
        st.success("✅ Your details have been saved successfully!")

    else:
        st.error("❌ Please enter your name and email.")
        st.write(st.secrets)  # This should print all secrets stored

import streamlit as st

# Print all secrets to verify it's loaded correctly
st.write(st.secrets)

# Print a specific secret to test
st.write(st.secrets["gspread_service_account"]["project_id"])






