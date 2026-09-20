import streamlit as st
import pandas as pd
from gtts import gTTS
import io
from PIL import Image
from google import genai

st.set_page_config(page_title="Reciprocity", page_icon="❤️", layout="centered")

# --- GEMINI SETUP - KOTHA SDK ---
try:
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=GEMINI_KEY)
    GEMINI_OK = True
except:
    GEMINI_OK = False
    client = None

LANG = {
    "English": {"s":"Simple - No Reading", "p":"Pro - Full Report", "up":"📸 Take Photo of Bill", "play":"🔊 PLAY MY SALE", "ask":"🎤 Ask"},
    "Telugu": {"s":"Simple - చదవడం రాదు", "p":"Pro - పూర్తి రిపోర్ట్", "up":"📸 బిల్ ఫోటో తీయండి", "play":"🔊 నా అమ్మకాలు వినండి", "ask":"🎤 అడగండి"},
    "Hindi": {"s":"Simple - पढ़ना नहीं आता", "p":"Pro - पूरी रिपोर्ट", "up":"📸 बिल की फोटो लो", "play":"🔊 मेरी बिक्री सुनो", "ask":"🎤 पूछो"},
    "Tamil": {"s":"Simple - படிக்கத் தெரியாது", "p":"Pro - முழு அறிக்கை", "up":"📸 பில் புகைப்படம் எடு", "play":"🔊 என் விற்பனையை கேள்", "ask":"🎤 கேள்"},
    "Kannada": {"s":"Simple - ಓದಲು ಬರಲ್ಲ", "p":"Pro - ಪೂರ್ಣ ವರದಿ", "up":"📸 ಬಿಲ್ ಫೋಟೋ ತೆಗೆಯಿರಿ", "play":"🔊 ನನ್ನ ಮಾರಾಟ ಕೇಳಿ", "ask":"🎤 ಕೇಳಿ"},
}

if 'mode' not in st.session_state: st.session_state['mode'] = None
if 'bill_text' not in st.session_state: st.session_state['bill_text'] = ""

def speak_text(text, lang_name):
    lang_code_map = {"English":"en","Telugu":"te","Hindi":"hi","Tamil":"ta","Kannada":"kn"}
    g_code = lang_code_map.get(lang_name, "en")
    try:
        tts = gTTS(text=text, lang=g_code, slow=False)
        buf = io.BytesIO(); tts.write_to_fp(buf); buf.seek(0)
        st.audio(buf, format='audio/mp3')
        st.success(f"🔊 {text}")
    except:
        tts = gTTS(text=text, lang='en', slow=False)
        buf = io.BytesIO(); tts.write_to_fp(buf); buf.seek(0)
        st.audio(buf, format='audio/mp3')

def read_real_bill(image_file):
    try:
        img = Image.open(image_file)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=["Read this Indian shop bill. Extract items, prices, total. Only what you see, don't make up. Format: Shop:... Items:... Total:...", img]
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"

if st.session_state['mode'] is None:
    st.markdown("<h1 style='text-align:center'>❤️ Reciprocity</h1><p style='text-align:center'>GIVE • TAKE • GROW TOGETHER</p>", unsafe_allow_html=True)
    if not GEMINI_OK:
        st.error("⚠️ GEMINI_API_KEY add cheyandi Secrets lo")
    else:
        st.success("✅ AI Bill Reader Ready - Nijamaina bill chaduvutundi!")

    lang = st.selectbox("🌐 Language / భాష", list(LANG.keys()))
    st.session_state['lang'] = lang
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"🟢 {LANG[lang]['s']}", use_container_width=True):
            st.session_state['mode'] = 'simple'; st.rerun()
    with col2:
        if st.button(f"🔵 {LANG[lang]['p']}", use_container_width=True):
            st.session_state['mode'] = 'pro'; st.rerun()
else:
    lang = st.session_state.get('lang', 'English')
    t = LANG[lang]
    if st.button("⬅️ Back"):
        st.session_state['mode'] = None; st.rerun()

    st.header(t['s'] if st.session_state['mode']=='simple' else t['p'])

    st.subheader(t['up'])
    tab1, tab2 = st.tabs(["📁 Upload", "📸 Camera"])
    bill_file = None
    with tab1:
        bill_file = st.file_uploader("Bill pettandi", type=['jpg','png','jpeg'])
    with tab2:
        cam_file = st.camera_input("Camera")
        if cam_file: bill_file = cam_file

    if bill_file:
        st.image(bill_file, caption="Bill", width=350)
        if GEMINI_OK:
            with st.spinner("🤖 Nee bill ni nijamga chaduvutonna..."):
                real_text = read_real_bill(bill_file)
                st.session_state['bill_text'] = real_text
            st.success("✅ Bill Read - Nijamaina data!")
            st.info(f"📄 **Bill lo unadi:**\n\n{st.session_state['bill_text']}")
            speak_text(st.session_state['bill_text'][:250], lang)

    st.divider()
    user_q = st.text_input("Bill gurinchi adagandi", placeholder="Ex: Total entha? Sugar entha?")
    if user_q and st.session_state['bill_text']:
        with st.spinner("Answering from YOUR bill..."):
            try:
                ans = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[f"Bill: {st.session_state['bill_text']}\nQuestion: {user_q}\nAnswer in {lang}, simple, only from bill"]
                )
                reply = ans.text
                st.write(f"**Answer:** {reply}")
                speak_text(reply, lang)
            except Exception as e:
                st.error(e)
    elif user_q:
        st.warning("Mundu bill pettandi")

    if st.button(t['play'], use_container_width=True) and st.session_state['bill_text']:
        speak_text(st.session_state['bill_text'], lang)
