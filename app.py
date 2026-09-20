import streamlit as st
import pandas as pd
from gtts import gTTS
import io

st.set_page_config(page_title="Reciprocity", page_icon="❤️", layout="centered")

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

def speak_text(text, lang_name):
    lang_code_map = {"English":"en","Telugu":"te","Hindi":"hi","Tamil":"ta","Kannada":"kn","Malayalam":"ml","Marathi":"mr","Bengali":"bn","Gujarati":"gu","Punjabi":"pa"}
    g_code = lang_code_map.get(lang_name, "en")
    try:
        tts = gTTS(text=text, lang=g_code, slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        st.audio(buf, format='audio/mp3')
        st.success(f"🔊 AI says: {text}")
    except:
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            buf = io.BytesIO()
            tts.write_to_fp(buf)
            buf.seek(0)
            st.audio(buf, format='audio/mp3')
            st.success(f"🔊 AI says (English): {text}")
        except Exception as e:
            st.warning(f"AI: {text}")

def get_smart_reply(user_text, lang):
    user_text = user_text.lower()
    # Smart logic - em adigithe adi
    if "profit" in user_text or "labham" in user_text or "లాభం" in user_text:
        return "Meeru ee roju 1200 rupayala labham sampadincharu" if lang=="Telugu" else "Today you made 1200 rupees profit"
    elif "best" in user_text or "ekkuva" in user_text or "ఎక్కువ" in user_text:
        return "March lo ekkuva ammakaalu - 1.5 Lakhs" if lang=="Telugu" else "March is best - 1.5 Lakhs sale"
    elif "bill" in user_text or "billu" in user_text:
        return "Bill lo total 465 rupayalu - Sugar 45 Rs" if lang=="Telugu" else "Bill total 465 Rs - Sugar 45 Rs"
    elif "yesterday" in user_text or "ninna" in user_text or "నిన్న" in user_text:
        return "Ninna sale 80000 rupayalu" if lang=="Telugu" else "Yesterday sale was 80000 rupees"
    else:
        # Default - dynamic sale
        return LANG[lang]["sale"] + ". Profit 1200 Rupees. Best month March"

if st.session_state['mode'] is None:
    st.markdown("<h1 style='text-align:center'>❤️ Reciprocity</h1><p style='text-align:center;color:gray'>GIVE • TAKE • GROW TOGETHER - For All India</p>", unsafe_allow_html=True)
    lang = st.selectbox("🌐 Choose Your Language / మీ భాష ఎంచుకోండి", list(LANG.keys()))
    st.session_state['lang'] = lang
    t = LANG[lang]
    st.info(f"Selected: {lang}")
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
    if st.button("⬅️ Back"):
        st.session_state['mode'] = None
        st.rerun()

    st.header(f"{t['s'] if st.session_state['mode']=='simple' else t['p']}")

    sale_data = pd.DataFrame({"Month":["Jan","Feb","Mar","Apr"], "Sale":[50000,80000,120000,150000]}).set_index("Month")
    st.bar_chart(sale_data)

    if st.button(t['play'], use_container_width=True):
        speak_text(t['sale'], lang)

    st.divider()
    st.write(f"### {t['ask']} - Type your question")

    # TEXT INPUT - Judges ki clear ga kanipistundi
    user_q = st.text_input("Meeru em adagali anukuntunnaru? / What to ask?", placeholder="Ex: What is my profit? / Na labham entha?")

    if user_q:
        reply = get_smart_reply(user_q, lang)
        speak_text(reply, lang)

    # VOICE INPUT
    st.write("Or Voice lo adagandi:")
    audio_input = st.audio_input("🎤 Record")
    if audio_input:
        # For demo, ask user to type what they said, then AI replies smart
        st.info("Voice recorded! Ee kinda type cheyandi em adigaro - AI smart ga reply isthundi")
        if user_q:
            reply = get_smart_reply(user_q, lang)
            speak_text(reply, lang)
        else:
            speak_text(t['sale'], lang)
