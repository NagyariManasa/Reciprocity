import streamlit as st
import pandas as pd

st.set_page_config(page_title="Reciprocity", page_icon="🤝", layout="centered")

# === ALL INDIAN LANGUAGES - 10 LANGUAGES ===
LANG = {
    "English": {"s":"Simple - No Reading", "p":"Pro - Full Report", "up":"📷 Take Photo of Bill", "play":"🔊 PLAY MY SALE", "sale":"Today sale is 5000 Rupees", "ask":"🎤 Speak to AI"},
    "Telugu": {"s":"Simple - చదువుకోని వారికి", "p":"Pro - చదువుకున్న వారికి", "up":"📷 బిల్ ఫోటో తీయండి", "play":"🔊 అమ్మకాలు వినండి", "sale":"ఈ రోజు అమ్మకాలు 5000 రూపాయలు", "ask":"🎤 AI తో మాట్లాడండి"},
    "Hindi": {"s":"Simple - अनपढ़ के लिए", "p":"Pro - पढ़े लिखे के लिए", "up":"📷 बिल की फोटो लो", "play":"🔊 बिक्री सुनो", "sale":"आज की बिक्री 5000 रुपये है", "ask":"🎤 AI से बोलो"},
    "Tamil": {"s":"Simple - படிக்காதவர்களுக்கு", "p":"Pro - படித்தவர்களுக்கு", "up":"📷 பில் புகைப்படம் எடு", "play":"🔊 விற்பனையை கேள்", "sale":"இன்று விற்பனை 5000 ரூபாய்", "ask":"🎤 AI யிடம் பேசு"},
    "Kannada": {"s":"Simple - ಓದದವರಿಗೆ", "p":"Pro - ಓದಿದವರಿಗೆ", "up":"📷 ಬಿಲ್ ಫೋಟೋ ತೆಗೆಯಿರಿ", "play":"🔊 ಮಾರಾಟ ಕೇಳಿ", "sale":"ಇಂದು ಮಾರಾಟ 5000 ರೂಪಾಯಿ", "ask":"🎤 AI ಜೊತೆ ಮಾತನಾಡಿ"},
    "Malayalam": {"s":"Simple - പഠിക്കാത്തവർക്ക്", "p":"Pro - പഠിച്ചവർക്ക്", "up":"📷 ബിൽ ഫോട്ടോ എടുക്കുക", "play":"🔊 വിൽപ്പന കേൾക്കുക", "sale":"ഇന്ന് വിൽപ്പന 5000 രൂപ", "ask":"🎤 AI യോട് സംസാരിക്കൂ"},
    "Marathi": {"s":"Simple - न शिकलेल्यांसाठी", "p":"Pro - शिकलेल्यांसाठी", "up":"📷 बिलाचा फोटो घ्या", "play":"🔊 विक्री ऐका", "sale":"आजची विक्री 5000 रुपये", "ask":"🎤 AI शी बोला"},
    "Bengali": {"s":"Simple - অশিক্ষিতদের জন্য", "p":"Pro - শিক্ষিতদের জন্য", "up":"📷 বিলের ছবি তুলুন", "play":"🔊 বিক্রয় শুনুন", "sale":"আজকের বিক্রি 5000 টাকা", "ask":"🎤 AI এর সাথে কথা বলুন"},
    "Gujarati": {"s":"Simple - અભણ માટે", "p":"Pro - ભણેલા માટે", "up":"📷 બિલનો ફોટો લો", "play":"🔊 વેચાણ સાંભળો", "sale":"આજનું વેચાણ 5000 રૂપિયા", "ask":"🎤 AI સાથે બોલો"},
    "Punjabi": {"s":"Simple - ਅਨਪੜ੍ਹ ਲਈ", "p":"Pro - ਪੜ੍ਹੇ ਲਿਖੇ ਲਈ", "up":"📷 ਬਿੱਲ ਦੀ ਫੋਟੋ ਲਓ", "play":"🔊 ਵਿਕਰੀ ਸੁਣੋ", "sale":"ਅੱਜ ਦੀ ਵਿਕਰੀ 5000 ਰੁਪਏ", "ask":"🎤 AI ਨਾਲ ਗੱਲ ਕਰੋ"},
}

if 'mode' not in st.session_state:
    st.session_state['mode'] = None

if st.session_state['mode'] is None:
    st.markdown("<h1 style='text-align:center'>🤝 Reciprocity</h1><p style='text-align:center;color:gray;letter-spacing:2px'>GIVE • TAKE • GROW TOGETHER - For All India</p>", unsafe_allow_html=True)
    lang = st.selectbox("🌐 Choose Your Language / अपनी भाषा चुनें / మీ భాష ఎంచుకోండి", list(LANG.keys()))
    st.session_state['lang'] = lang
    t = LANG[lang]
    st.info(f"Selected: {lang} - {len(LANG)} languages available!")
    c1,c2 = st.columns(2)
    with c1:
        st.markdown(f"### 🧓 {t['s']}")
        if st.button("🧓 SIMPLE MODE", use_container_width=True, type="primary"):
            st.session_state['mode']='simple'
            st.rerun()
    with c2:
        st.markdown(f"### 🎓 {t['p']}")
        if st.button("🎓 PRO MODE", use_container_width=True):
            st.session_state['mode']='pro'
            st.rerun()
    st.stop()

lang = st.session_state.get('lang','English')
t = LANG[lang]
st.button("⬅️ Back", on_click=lambda: st.session_state.update({'mode':None}))

if st.session_state['mode'] == 'simple':
    st.title(t['up'])
    st.camera_input("Camera")
    st.file_uploader("Or Upload Photo", type=['jpg','png'])
    st.divider()
    if st.button(t['play'], use_container_width=True, type="primary"):
        st.success(f"🔊 {t['sale']}")
        st.balloons()
    st.subheader(t['ask'])
    v = st.audio_input("🎤 Press to Speak")
    if v:
        st.success(f"✅ Voice OK! AI says: {t['sale']}")

else:
    st.title(f"📊 Pro Dashboard - {lang}")
    c1,c2,c3 = st.columns(3)
    c1.metric("Revenue","₹1,20,000","12% ↑")
    c2.metric("Profit","₹35,000","8% ↑")
    c3.metric("Top Product","Rice")
    st.bar_chart(pd.DataFrame({'Month':['Jan','Feb','Mar'],'Sale':[50000,80000,120000]}).set_index('Month'))
    st.divider()
    st.subheader(f"🤖 Gemini AI - Ask in {lang}")
    q = st.text_input(f"Type in {lang} - Ex: Best month?")
    if q:
        try:
            import google.generativeai as genai
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"User speaks {lang}. Answer only in {lang}. Shop data: Revenue 1.2L, Profit 35k. Question: {q}"
            res = model.generate_content(prompt)
            st.success(res.text)
        except:
            st.warning(f"Demo Answer in {lang}: December is best month with ₹1.5L sales! (Add GEMINI_API_KEY in Streamlit Secrets for real AI)")
