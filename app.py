import streamlit as st
import google.generativeai as genai
import datetime
import base64
import os

# --- Page Config ---
st.set_page_config(page_title="Railway Letter Generator", page_icon="🚆", layout="wide")

# --- Function to Load Image ---
def get_local_image_base64(file_path):
    try:
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded_string}"
    except:
        return None

# --- CSS Styles (A4 Layout) ---
a4_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700&display=swap');
.a4-container {
    width: 210mm; min-height: 297mm; padding: 20mm; margin: 10mm auto;
    background: white; font-family: 'Merriweather', serif; color: #333;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
}
.header-center { text-align: center; font-weight: bold; font-size: 24px; text-transform: uppercase; margin-bottom: 30px; color: #000; }
.top-right-info { text-align: right; margin-bottom: 40px; font-weight: bold; }
.left-info { text-align: left; margin-bottom: 20px; }
.subject-line { font-weight: bold; margin-top: 15px; margin-bottom: 25px; }
.letter-body { text-align: justify; line-height: 1.6; margin-bottom: 50px; white-space: pre-wrap; }
.signature-block { float: right; text-align: center; width: 250px; margin-top: 20px; }
.signature-image { max-width: 150px; max-height: 100px; margin: 10px auto; display: block; }
.signatory-name { font-weight: bold; margin-top: 5px; }
.signatory-desig { font-weight: bold; }

/* प्रिंट करताना फक्त पत्र दिसावे */
@media print {
    body * { visibility: hidden; }
    .a4-container, .a4-container * { visibility: visible; }
    .a4-container { position: absolute; left: 0; top: 0; margin: 0; padding: 20mm !important; box-shadow: none; }
    .stApp > header, .stApp > footer, .stSidebar { display: none !important; }
}
</style>
"""

# --- MAIN APP ---
st.sidebar.title("⚙️ Settings")
# टीप: GitHub वर टाकताना आपली API Key इथे हार्डकोड करू नका, ती Input मध्येच ठेवा.
api_key = st.sidebar.text_input("Gemini API Key", type="password")

st.title("🚆 Railway Letter Generator")

with st.sidebar.form("inputs"):
    letter_date = st.date_input("Select Date", datetime.date.today())
    to_address = st.text_area("To (Recipient)", height=100, placeholder="The DRM,\nCentral Railway...")
    subject_text = st.text_input("Subject")
    instructions = st.text_area("Details for Letter Body", height=150)
    submitted = st.form_submit_button("Generate Letter")

if submitted:
    if not api_key:
        st.error("Please enter Gemini API Key first!")
    else:
        with st.spinner("Generating letter..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-pro')
                prompt = f"Write ONLY body for railway letter. To: {to_address}, Sub: {subject_text}, Details: {instructions}. Tone: Formal Official."
                response = model.generate_content(prompt)
                
                # सही ऑटोमॅटिक घेणे (signature.png)
                sig_img = get_local_image_base64("signature.png")
                sig_html = f'<img src="{sig_img}" class="signature-image">' if sig_img else "<br><small style='color:red'>signature.png missing</small><br>"

                final_html = f"""
                {a4_css}
                <div class="a4-container">
                    <div class="header-center">Central Railway</div>
                    <div class="top-right-info">TI/O/KRD<br>Date: {letter_date.strftime("%d/%m/%Y")}</div>
                    <div class="left-info">To,<br>{to_address.replace(chr(10), '<br>')}</div>
                    <div class="subject-line">Sub: {subject_text}</div>
                    <div class="letter-body">{response.text}</div>
                    <div class="signature-block">Yours Faithfully,{sig_html}
                    <div class="signatory-name">R.H.Wankhede</div>
                    <div class="signatory-desig">TI/KRD</div></div>
                    <div style="clear: both;"></div>
                </div>
                """
                st.markdown(final_html, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")
