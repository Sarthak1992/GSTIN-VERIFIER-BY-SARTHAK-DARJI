import streamlit as st
import requests
from fpdf import FPDF
import datetime

# --- FIRM SETTINGS ---
FIRM_NAME = "CA Sarthak Darji"

# --- PDF GENERATOR ---
class GSTReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.set_text_color(0, 74, 153)
        self.cell(0, 10, FIRM_NAME, ln=True, align='L')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, "Chartered Accountant | Verification Report", ln=True, align='L')
        self.line(10, 28, 200, 28)
        self.ln(10)

# --- MAIN APP ---
st.set_page_config(page_title=FIRM_NAME, page_icon="⚖️")
st.title("🔍 GSTIN Validator")
st.write(f"Professional Utility by **{FIRM_NAME}**")

gstin_input = st.text_input("Enter 15-digit GSTIN").upper().strip()

if st.button("Verify GSTIN"):
    if len(gstin_input) == 15:
        # This new API uses a GET request with query parameters
        url = "https://india-gstin-validator.p.rapidapi.com/validate"
        querystring = {"gstin": gstin_input}
        
        headers = {
            "x-rapidapi-key": st.secrets["RAPID_API_KEY"],
            "x-rapidapi-host": "india-gstin-validator.p.rapidapi.com"
        }

        with st.spinner("Connecting to Government Portal..."):
            try:
                # Note the change to 'get' and 'params'
                response = requests.get(url, headers=headers, params=querystring)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get("valid") == True:
                        st.success("✅ Valid GSTIN Found!")
                        st.json(result)
                        
                        # (PDF generation code would go here similarly to previous versions)
                    else:
                        st.error("❌ This GSTIN is INVALID according to the portal.")
                else:
                    st.error(f"Error: {response.status_code}. Check your API subscription.")
            except Exception as e:
                st.error(f"Connection Error: {e}")
    else:
        st.warning("Please enter a valid 15-digit GSTIN.")
