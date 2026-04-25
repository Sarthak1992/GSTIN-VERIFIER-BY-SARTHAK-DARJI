import streamlit as st
import requests
from fpdf import FPDF
import datetime

# --- SETTINGS ---
FIRM_NAME = "CA Sarthak Darji"
# PASTE YOUR KEY HERE
RAPID_API_KEY = "YOUR_ACTUAL_KEY_FROM_RAPIDAPI" 

# --- PDF GENERATOR ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, FIRM_NAME, ln=True, align='L')
        self.line(10, 20, 200, 20)
        self.ln(10)

def generate_pdf(data, gstin):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"GST Verification Report for: {gstin}", ln=True)
    pdf.set_font("Arial", '', 11)
    
    # Extracting data from API response
    info = data.get('data', {})
    content = {
        "Business Name": info.get('lgnm', 'Not Found'),
        "Status": info.get('sts', 'Unknown'),
        "Type": info.get('dty', 'Unknown'),
        "Date of Reg": info.get('rgdt', 'N/A')
    }
    
    for key, val in content.items():
        pdf.cell(50, 10, f"{key}: {val}", ln=True)
    
    return pdf.output(dest='S').encode('latin-1')

# --- WEBSITE INTERFACE ---
st.set_page_config(page_title=FIRM_NAME)
st.title("⚖️ GST Bill Verifier")
st.write(f"Digital Utility by **{FIRM_NAME}**")

gstin = st.text_input("Enter Shop's GSTIN (15 Digits)").upper().strip()

if st.button("Check & Verify"):
    if len(gstin) == 15:
        url = "https://india-gst-validator-business-search.p.rapidapi.com/"
        headers = {
            "Content-Type": "application/json",
            "x-rapidapi-key": RAPID_API_KEY,
            "x-rapidapi-host": "india-gst-validator-business-search.p.rapidapi.com"
        }
        
        with st.spinner("Checking records..."):
            response = requests.post(url, json={"gstin": gstin}, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                biz_name = result.get('data', {}).get('lgnm', 'Unknown')
                st.success(f"Business Found: {biz_name}")
                
                # Show Result Logic
                st.write(result)
                
                # PDF Download
                report_bytes = generate_pdf(result, gstin)
                st.download_button("Download Report PDF", report_bytes, f"{gstin}.pdf")
            else:
                st.error("API Connection Failed. Check your Key.")
    else:
        st.warning("Please enter a valid 15-digit GSTIN.")
        # Final check
