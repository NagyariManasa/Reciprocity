import streamlit as st
import pandas as pd
from gtts import gTTS
import io

st.set_page_config(page_title="Reciprocity", page_icon="❤️", layout="centered")

# --- ALL INDIAN LANGUAGES - 10 LANGUAGES ---
LANG = {
    "English": {"s":"Simple - No Reading", "p":"Pro - Full Report", "up":"📸 Take Photo of Bill", "play":"🔊 PLAY MY SALE", "sale":"Today sale is 5000 Rupees", "ask":"🎤 Ask"},
    "Telugu": {"s":"Simple - చదవడం రాదు", "p":"Pro - పూర్తి రిపోర్ట్", "up":"📸 బిల్ ఫోటో తీయండి", "play":"🔊 నా అమ్మకాలు వినండి", "sale":"ఈ రోజు అమ్మకాలు 5000 రూపాయలు", "ask":"🎤 అడగండి"},
    "Hindi": {"s":"Simple - पढ़ना नहीं आता", "p":"Pro - पूरी रिपोर्ट", "up":"📸 बिल की फोटो लो", "play":"🔊 मेरी बिक्री सुनो", "sale":"आज की बिक्री 5000 रुपये है", "ask":"🎤 पूछो"},
    "Tamil": {"s":"Simple - படிக்கத் தெரியாது", "p":"Pro - முழு அறிக்கை", "up":"📸 பில் புகைப்படம் எடு", "play":"🔊 என் விற்பனையை கேள்", "sale":"இன்றைய விற்பனை 5000 ரூபாய்", "ask":"🎤 கேள்"},
    "Kannada": {"s":"Simple - ಓದಲು ಬರಲ್ಲ", "p":"Pro - ಪೂರ್ಣ ವರದಿ", "up":"📸 ಬಿಲ್ ಫೋಟೋ ತೆಗೆಯಿರಿ", "play":"🔊 ನನ್ನ ಮಾರಾಟ ಕೇಳಿ", "sale":"ಇಂದಿನ ಮಾರಾಟ 5000 ರೂಪಾಯಿ", "ask":"🎤 ಕೇಳಿ"},
    "Malayalam": {"s":"Simple - വായിക്കാൻ അറിയില്ല", "p":"Pro - പൂർണ്ണ റിപ്പോർട്ട്", "up":"📸 ബില്ലിന്റെ ഫോട്ടോ എടുക്കൂ", "play":"🔊 എന്റെ വിൽപ്പന കേൾക്കൂ", "sale":"ഇന്നത്തെ വിൽപ്പന 5000 രൂപ", "ask":"🎤 ചോദിക്കൂ"},
    "Marathi": {"s":"Simple - वाचता येत नाही", "p":"Pro - पूर्ण अहवाल", "up":"📸 बिलाचा फोटो घ्या", "play":"🔊 माझी विक्री ऐका", "sale":"आजची विक्री 5000 रुपये आहे", "ask":"🎤 विचारा"},
    "Bengali": {"s":"Simple - পড়তে পারি না", "p":"Pro - সম্পূর্ণ রিপোর্ট", "up":"📸 বিলের ছবি তুলুন", "play":"🔊 আমার বিক্রি শুনুন", "sale":"আজ বিক্রি 5000 টাকা", "ask":"🤖 জিজ্ঞাসা"},
    "Gujarati": {"s":"Simple - વાંચતા આવડતું નથી", "p":"Pro - પૂરો રિપોર્ટ", "up":"📸 બિલનો ફોટો લો", "play":"🔊 મારું વેચાણ સાંભળો", "sale":"આજનું વેચાણ 5000 રૂપિયા", "ask":"🎤 પૂછો"},
    "Punjabi": {"s":"Simple - ਪੜ੍ਹਨਾ ਨਹੀਂ ਆਉਂਦਾ", "p":"Pro - ਪੂਰੀ ਰਿਪੋਰਟ", "up":"📸 ਬਿੱਲ ਦੀ ਫੋਟੋ ਲਓ", "play":"🔊 ਮੇਰੀ ਵਿਕਰੀ ਸੁਣੋ", "sale":"ਅੱਜ ਦੀ ਵਿਕਰੀ 5000 ਰੁਪਏ ਹੈ", "ask":"🎤 ਪੁੱਛੋ"},
}

if 'mode' not in st.session_state:
    st.session_state['mode'] = None

if st.session_state['mode'] is None:
    st.markdown("<h1 style='text-align:center'>❤️ Reciprocity</h1><p style='text-align:center;color:gray;letter-spacing:2px'>GIVE • TAKE • GROW TOGETHER - For All India</p>", unsafe_allow_html=True)
    st.markdown("### 🌐 Choose Your Language / మీ భాష ఎంచుకోండి")
    lang = st.selectbox("", list(LANG.keys()))
    st.session_state['lang'] = lang
    t = LANG[lang]
    st.info(f"Selected: {lang} - {len(LANG)} languages available!")

    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"🟢 {t['s']}", use_container_width=True):
            st.session_state['mode'] = 'simple'
            st.rerun()
    with col2:
        if st.button(f"🔵 {t['p']}", use_container_width=True):
            st.session_state['mode'] = 'pro'
            st.rerun()
else:
    lang = st.session_state.get('lang', 'Telugu')
    t = LANG[lang]

    if st.button("⬅️ Back / Change Language"):
        st.session_state['mode'] = None
        st.rerun()

    # --- VOICE PLAY FUNCTION - FIX FOR PHONE ---
    def speak_text(text, lang_name):
        lang_code_map = {"English":"en","Telugu":"te","Hindi":"hi","Tamil":"ta","Kannada":"kn","Malayalam":"ml","Marathi":"mr","Bengali":"bn","Gujarati":"gu","Punjabi":"pa"}
        g_code = lang_code_map.get(lang_name, "en")
        try:
            tts = gTTS(text=text, lang=g_code, slow=False)
            buf = io.BytesIO()
            tts.write_to_fp(buf)
            buf.seek(0)
            st.audio(buf, format='audio/mp3', autoplay=False)
            st.success(f"🔊 Voice OK! AI says: {text}")
        except Exception as e:
            st.warning(f"Voice text: {text} - Audio error: {e}")
            # Fallback English if regional fails
            try:
                tts = gTTS(text=text, lang='en', slow=False)
                buf = io.BytesIO()
                tts.write_to_fp(buf)
                buf.seek(0)
                st.audio(buf, format='audio/mp3')
            except:
                pass

    # --- SIMPLE MODE ---
    if st.session_state['mode'] == 'simple':
        st.header(f"🟢 {t['s']}")

        st.subheader(t['up'])
        bill_file = st.file_uploader("Upload Bill", type=['jpg','png','jpeg'])
        if bill_file:
            st.image(bill_file, caption="Bill uploaded!", width=300)
            st.success("AI Reading Bill... Sugar 45 Rs, Oil 120 Rs - Total 465 Rs")

        st.divider()
        # Sale Data
        sale_data = pd.DataFrame({"Month":["Jan","Feb","Mar"], "Sale":[50000,80000,120000]}).set_index("Month")
        st.bar_chart(sale_data)
        st.metric("Best Month", "March", "₹1.5L Sales")
        st.caption("Add GEMINI_API_KEY in Streamlit Secrets for real AI")

        st.divider()
        if st.button(t['play'], use_container_width=True):
            speak_text(t['sale'], lang)

        st.write(f"### {t['ask']} about sale?")
        audio_input = st.audio_input("🎤 Record your voice")
        if audio_input:
            st.success(f"Voice OK! You asked about sale!")
            speak_text(t['sale'], lang)

    # --- PRO MODE ---
    else:
        st.header(f"🔵 {t['p']}")
        st.write("Full Business Dashboard")

        sale_data = pd.DataFrame({"Month":["Jan","Feb","Mar","Apr"], "Sale":[50000,80000,120000,150000]}).set_index("Month")
        st.bar_chart(sale_data)
        st.line_chart(sale_data)

        if st.button(t['play'], use_container_width=True):
            speak_text(t['sale'], lang)
