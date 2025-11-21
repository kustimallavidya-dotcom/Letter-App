import streamlit as st
from openai import OpenAI
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="Railway Letter Generator", page_icon="🚆", layout="centered")

# --- CSS Styles (A4 Paper Look) - जसेच्या तसे ठेवले आहे ---
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

# --- API Key Setup (DeepSeek) ---
# Streamlit Secrets मधून Key घेईल. नाव: DEEPSEEK_API_KEY
if "DEEPSEEK_API_KEY" in st.secrets:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
else:
    st.error("API Key सापडली नाही. कृपया Streamlit Secrets मध्ये 'DEEPSEEK_API_KEY' ॲड करा.")
    st.stop()

# DeepSeek Client Setup
try:
    client = OpenAI(
        api_key=api_key, 
        base_url="https://api.deepseek.com"
    )
except Exception as e:
    st.error(f"Connection Error: {e}")
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
st.title("🚆 Railway Letter Generator (DeepSeek)")

if submitted:
    if not details:
        st.warning("Please enter details for the letter.")
    else:
        with st.spinner("Generating professional letter with DeepSeek..."):
            try:
                # Prompt Drafting
                system_prompt = "You are a professional assistant for Indian Railways employees. Write a formal official letter. Use standard Indian official letter format. Output ONLY the HTML content for the letter body paragraphs. Do not output markdown code blocks."
                
                user_prompt = f"""
                Details for the letter:
                Date: {letter_date.strftime('%d-%m-%Y')}
                To: {recipient}
                Subject: {subject}
                Details: {details}
                
                Keep the tone professional, polite, and formal.
                """

                # DeepSeek Call
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    stream=False
                )
                
                # Extracting Text
                letter_content = response.choices[0].message.content
                
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
