import streamlit as st
import pandas as pd
from gtts import gTTS
import io
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="Reciprocity", page_icon="❤️", layout="centered")

# --- GEMINI SETUP ---
try:
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    GEMINI_OK = True
except:
    GEMINI_OK = False
    model = None

LANG = {
    "English": {"s":"Simple - No Reading", "p":"Pro - Full Report", "up":"📸 Take Photo of Bill", "play":"🔊 PLAY MY SALE", "ask":"🎤 Ask"},
    "Telugu": {"s":"Simple - చదవడం రాదు", "p":"Pro - పూర్తి రిపోర్ట్", "up":"📸 బిల్ ఫోటో తీయండి", "play":"🔊 నా అమ్మకాలు వినండి", "ask":"🎤 అడగండి"},
    "Hindi": {"s":"Simple - पढ़ना नहीं आता", "p":"Pro - पूरी रिपोर्ट", "up":"📸 बिल की फोटो लो", "play":"🔊 मेरी बिक्री सुनो", "ask":"🎤 पूछो"},
    "Tamil": {"s":"Simple - படிக்கத் தெரியாது", "p":"Pro - முழு அறிக்கை", "up":"📸 பில் புகைப்படம் எடு", "play":"🔊 என் விற்பனையை கேள்", "ask":"🎤 கேள்"},
    "Kannada": {"s":"Simple - ಓದಲು ಬರಲ್ಲ", "p":"Pro - ಪೂರ್ಣ ವರದಿ", "up":"📸 ಬಿಲ್ ಫೋಟೋ ತೆಗೆಯಿರಿ", "play":"🔊 ನನ್ನ ಮಾರಾಟ ಕೇಳಿ", "ask":"🎤 ಕೇಳಿ"},
    "Malayalam": {"s":"Simple - വായിക്കാൻ അറിയില്ല", "p":"Pro - പൂർണ്ണ റിപ്പോർട്ട്", "up":"📸 ബില്ലിന്റെ ഫോട്ടോ എടുക്കൂ", "play":"🔊 എന്റെ വിൽപ്പന കേൾക്കൂ", "ask":"🎤 ചോദിക്കൂ"},
    "Marathi": {"s":"Simple - वाचता येत नाही", "p":"Pro - पूर्ण अहवाल", "up":"📸 बिलाचा फोटो घ्या", "play":"🔊 माझी विक्री ऐका", "ask":"🎤 विचारा"},
    "Bengali": {"s":"Simple - পড়তে পারি না", "p":"Pro - সম্পূর্ণ রিপোর্ট", "up":"📸 বিলের ছবি তুলুন", "play":"🔊 আমার বিক্রি শুনুন", "ask":"🤖 জিজ্ঞাসা"},
    "Gujarati": {"s":"Simple - વાંચતા આવડતું નથી", "p":"Pro - પૂરો રિપોર્ટ", "up":"📸 બિલનો ફોટો લો", "play":"🔊 મારું વેચાણ સાંભળો", "ask":"🎤 પૂછો"},
    "Punjabi": {"s":"Simple - ਪੜ੍ਹਨਾ ਨਹੀਂ ਆਉਂਦਾ", "p":"Pro - ਪੂਰੀ ਰਿਪੋਰਟ", "up":"📸 ਬਿੱਲ ਦੀ ਫੋਟੋ ਲਓ", "play":"🔊 ਮੇਰੀ ਵਿਕਰੀ ਸੁਣੋ", "ask":"🎤 ਪੁੱਛੋ"},
}

if 'mode' not in st.session_state: st.session_state['mode'] = None
if 'bill_text' not in st.session_state: st.session_state['bill_text'] = ""
if 'bill_data' not in st.session_state: st.session_state['bill_data'] = ""

def speak_text(text, lang_name):
    lang_code_map = {"English":"en","Telugu":"te","Hindi":"hi","Tamil":"ta","Kannada":"kn","Malayalam":"ml","Marathi":"mr","Bengali":"bn","Gujarati":"gu","Punjabi":"pa"}
    g_code = lang_code_map.get(lang_name, "en")
    try:
        tts = gTTS(text=text, lang=g_code, slow=False)
        buf = io.BytesIO(); tts.write_to_fp(buf); buf.seek(0)
        st.audio(buf, format='audio/mp3')
        st.success(f"🔊 {text}")
    except:
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            buf = io.BytesIO(); tts.write_to_fp(buf); buf.seek(0)
            st.audio(buf, format='audio/mp3')
            st.success(f"🔊 {text}")
        except: st.warning(text)

def read_real_bill(image_file):
    """Nijamaina bill ni Gemini tho chadavadam"""
    try:
        img = Image.open(image_file)
        prompt = """
        You are a shop bill reader. Read this Indian shop bill image carefully.
        Extract:
        1. All items with price
        2. Total amount
        3. Shop name if visible
        Return in simple format like:
        Items: Sugar 45 Rs, Oil 120 Rs...
        Total: 465 Rs
        Do NOT make up. Only what you see in image.
        If unclear, say what you can read.
        """
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"Error reading bill: {e}"

if st.session_state['mode'] is None:
    st.markdown("<h1 style='text-align:center'>❤️ Reciprocity</h1><p style='text-align:center;color:gray'>GIVE • TAKE • GROW TOGETHER</p>", unsafe_allow_html=True)
    if not GEMINI_OK:
        st.error("⚠️ GEMINI_API_KEY add cheyandi Streamlit Secrets lo - app settings > Secrets")
    else:
        st.success("✅ AI Bill Reader Ready!")
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
    lang = st.session_state.get('lang', 'Telugu')
    t = LANG[lang]
    if st.button("⬅️ Back"):
        st.session_state['mode'] = None; st.rerun()

    st.header(t['s'] if st.session_state['mode']=='simple' else t['p'])

    # --- REAL BILL UPLOAD ---
    st.subheader(t['up'])
    if not GEMINI_OK:
        st.warning("Add GEMINI_API_KEY in Secrets for real bill reading")

    tab1, tab2 = st.tabs(["📁 Upload File", "📸 Camera"])
    bill_file = None
    with tab1:
        bill_file = st.file_uploader("Bill pettandi", type=['jpg','png','jpeg'], key="file")
    with tab2:
        cam_file = st.camera_input("Camera")
        if cam_file: bill_file = cam_file

    if bill_file:
        st.image(bill_file, caption="Bill uploaded", width=300)
        if GEMINI_OK:
            with st.spinner("🤖 AI bill chaduvutondi... Nijamaina bill reading..."):
                real_text = read_real_bill(bill_file)
                st.session_state['bill_text'] = real_text
                st.session_state['bill_data'] = real_text
            st.success("✅ Bill Read!")
            st.info(f"📄 **Bill lo unadi:**\n\n{st.session_state['bill_text']}")
            # Voice lo kuda cheppu
            speak_text(st.session_state['bill_text'][:200], lang) # first 200 chars
        else:
            st.image(bill_file)
            st.warning("API key ledu - manual ga type cheyandi")
            manual = st.text_input("Bill total entha? Type cheyandi")
            if manual:
                st.session_state['bill_text'] = f"Total {manual} Rs"
                st.session_state['bill_data'] = manual

    st.divider()
    sale_data = pd.DataFrame({"Month":["Jan","Feb","Mar","Apr"], "Sale":[50000,80000,120000,150000]}).set_index("Month")
    st.bar_chart(sale_data)

    st.divider()
    st.write(f"### {t['ask']} about THIS bill")

    # --- BILL MEEDA ADAGALI ---
    user_q = st.text_input("Bill gurinchi em adagali?", placeholder="Ex: Ee bill lo Sugar entha? / Total entha?")

    if user_q and st.session_state['bill_text']:
        if GEMINI_OK:
            with st.spinner("AI answering from YOUR bill..."):
                try:
                    prompt2 = f"Based on THIS bill only: {st.session_state['bill_text']}\n\nUser question: {user_q}\nAnswer in {lang} language, simple. Only from bill, don't make up."
                    ans = model.generate_content(prompt2)
                    reply = ans.text
                    st.write(f"**Answer:** {reply}")
                    speak_text(reply, lang)
                except Exception as e:
                    st.error(e)
        else:
            reply = f"Bill lo: {st.session_state['bill_text']}"
            speak_text(reply, lang)
    elif user_q:
        st.warning("Mundu bill pettandi - taruvata adagandi")

    if st.button(t['play'], use_container_width=True) and st.session_state['bill_text']:
        speak_text(st.session_state['bill_text'], lang)
