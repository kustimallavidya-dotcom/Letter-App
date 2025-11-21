import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="Railway Letter Generator", page_icon="🚆", layout="centered")

# --- CSS Styles (A4 Paper Look) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Times+New+Roman&display=swap');
    
    .main {
        background-color: #f0f2f6;
    }
    .a4-container {
        background-color: white;
        padding: 40px;
        margin: auto;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        font-family: 'Times New Roman', serif;
        font-size: 12pt;
        line-height: 1.5;
        color: black;
        min-height: 800px;
    }
    .header-center { text-align: center; font-weight: bold; margin-bottom: 20px; }
    .text-right { text-align: right; }
    .subject-line { font-weight: bold; margin: 20px 0; }
    .letter-body { text-align: justify; white-space: pre-wrap; }
    .footer { margin-top: 40px; text-align: right; }
    
    /* Print Settings */
    @media print {
        body * { visibility: hidden; }
        .a4-container, .a4-container * { visibility: visible; }
        .a4-container { position: absolute; left: 0; top: 0; width: 100%; margin: 0; padding: 20px; box-shadow: none; }
        .stApp > header, .stApp > footer, .stSidebar { display: none; }
    }
    </style>
""", unsafe_allow_html=True)

# --- API Key Setup (Automatic) ---
# ही सेटिंग तुमच्या Streamlit Secrets मधून Key घेईल
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key सापडली नाही. कृपया Streamlit Settings > Secrets मध्ये Key ॲड करा.")
    st.stop()

# --- Sidebar Inputs ---
st.sidebar.title("📝 Letter Details")
with st.sidebar.form("letter_form"):
    letter_date = st.date_input("Date", datetime.today())
    recipient = st.text_area("To (Recipient Details)", "The DRM,\nCentral Railway,\nNagpur Division.")
    subject = st.text_input("Subject", "Request for...")
    details = st.text_area("Letter Details (Points)", "Please write a letter regarding my leave application...")
    
    submitted = st.form_submit_button("Generate Letter 🚆")

# --- Main App Logic ---
st.title("🚆 Railway Letter Generator")

if submitted:
    if not details:
        st.warning("Please enter details for the letter.")
    else:
        with st.spinner("Generating professional letter..."):
            try:
                # Model Setup
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Prompt for AI
                prompt = f"""
                You are a professional assistant for Indian Railways employees.
                Write a formal official letter based on these details:
                
                Date: {letter_date.strftime('%d-%m-%Y')}
                To: {recipient}
                Subject: {subject}
                Details: {details}
                
                Format:
                - Use standard Indian official letter format.
                - Keep the tone professional, polite, and formal.
                - Do not include placeholders like [Your Name] inside the body if not provided, just leave space for signature.
                - Output ONLY the HTML content for the letter body (paragraphs), do not output markdown code blocks.
                """
                
                response = model.generate_content(prompt)
                letter_content = response.text
                
                # Display Letter on "A4 Paper"
                st.markdown(f"""
                    <div class="a4-container">
                        <div class="text-right"><strong>Date:</strong> {letter_date.strftime('%d-%m-%Y')}</div>
                        <br>
                        <div style="white-space: pre-wrap;"><strong>To,</strong><br>{recipient}</div>
                        <br>
                        <div class="subject-line">Sub: {subject}</div>
                        <br>
                        <div class="letter-body">
                            {letter_content}
                        </div>
                        <br><br>
                        <div class="footer">
                            <strong>Yours Faithfully,</strong>
                            <br><br><br>
                            (Signature)
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.success("Letter generated successfully!")
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

else:
    st.info("👈 डाव्या बाजूला माहिती भरा आणि 'Generate Letter' वर क्लिक करा.")
