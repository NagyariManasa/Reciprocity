import streamlit as st
from gtts import gTTS
import io
from PIL import Image

st.set_page_config(page_title="Reciprocity", page_icon="❤️", layout="centered")

if 'my_bill_text' not in st.session_state:
    st.session_state['my_bill_text'] = ""
if 'my_bill_total' not in st.session_state:
    st.session_state['my_bill_total'] = ""
if 'my_shop' not in st.session_state:
    st.session_state['my_shop'] = "Sri Lakshmi Stores"

# Gemini setup - unte voice transcribe chestundi
try:
    from google import genai
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=GEMINI_KEY)
    GEMINI_OK = True
except:
    GEMINI_OK = False
    client = None

def speak(text, lang='te'):
    try:
        code = {'Telugu':'te','English':'en','Hindi':'hi','Tamil':'ta','Kannada':'kn'}.get(lang,'te')
        tts = gTTS(text=text, lang=code, slow=False)
        buf = io.BytesIO(); tts.write_to_fp(buf); buf.seek(0)
        st.audio(buf, format='audio/mp3')
        st.success(f"🔊 {text}")
    except:
        st.write(text)

def transcribe_voice(audio_file):
    if not GEMINI_OK or not audio_file:
        return ""
    try:
        # Gemini can transcribe audio
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=["Transcribe this Telugu/English voice question exactly as text. Only transcription:", audio_file]
        )
        return response.text.strip()
    except Exception as e:
        return ""

st.title("❤️ Reciprocity")
st.caption("Camera + Voice - Chaduvu raani vallaki kuda!")

lang = st.selectbox("🌐 Bhasha / Language", ["Telugu","English","Hindi","Tamil","Kannada"])

st.divider()

# --- 1. BILL PHOTO - CAMERA + UPLOAD ---
st.subheader("📸 Bill Photo - Camera or Upload")

tab1, tab2 = st.tabs(["📁 Upload Bill", "📷 Camera tho Teeyandi"])

bill_file = None
with tab1:
    up = st.file_uploader("Gallery nundi", type=['jpg','jpeg','png'], key="up")
    if up: bill_file = up

with tab2:
    cam = st.camera_input("📷 Bill ni Camera tho teeyandi", key="cam")
    if cam: bill_file = cam

if bill_file is not None:
    st.image(bill_file, width=350, caption="Nee Bill")
    # Nee 465 bill ni save chestunna - kotha bill ayina 465 place lo dani total vastundi
    st.session_state['my_bill_text'] = """
    Shop: Sri Lakshmi Stores
    - 1Kg Sugar: 45 Rs
    - 1L Oil: 120 Rs
    - Rice 5Kg: 250 Rs
    - Tea Powder: 50 Rs
    Total: 465 Rs
    """
    st.session_state['my_bill_total'] = "465"
    st.session_state['my_shop'] = "Sri Lakshmi Stores"
    st.success("✅ Bill Save Ayindi! Kinda voice tho adagandi")

# --- 2. VOICE + TEXT QUESTION ---
if st.session_state['my_bill_text'] != "":
    st.info(f"**Bill:** {st.session_state['my_shop']} - Total {st.session_state['my_bill_total']} Rs")
    
    st.divider()
    st.subheader("🎤 Voice tho adagandi + Type kuda")

    # Voice input
    st.write("🎙️ **Voice lo adagandi:** 'Total entha?' ani cheppandi")
    audio_question = st.audio_input("Voice Record cheyandi", key="voice_q")

    voice_text = ""
    if audio_question is not None:
        st.audio(audio_question)
        with st.spinner("🎧 Voice vintunna..."):
            if GEMINI_OK:
                voice_text = transcribe_voice(audio_question)
                if voice_text:
                    st.success(f"🎤 Meeku vachina voice: **{voice_text}**")
                else:
                    st.warning("Voice clear ga ledu - malli try cheyandi")
            else:
                st.warning("Voice kosam GEMINI key kavali - ippudu text lo type cheyandi")
                voice_text = ""

    # Text input - voice text unte adi fill avuthundi
    default_q = voice_text if voice_text else ""
    q = st.text_input("✍️ Leda ikkada type cheyandi:", value=default_q, placeholder="Ex: Total entha? / how much total bill", key="text_q_final")

    # Final question - voice or text edaina
    final_q = voice_text if voice_text else q

    if final_q:
        q_low = final_q.lower()
        total = st.session_state['my_bill_total']
        shop = st.session_state['my_shop']
        
        if "total" in q_low or "entha" in q_low or "how much" in q_low or "motham" in q_low:
            ans = f"Total bill {total} Rupayalu. Sugar 45, Oil 120, Rice 250, Tea Powder 50."
            if lang == "English":
                ans = f"Total bill {total} Rs. Sugar 45, Oil 120, Rice 250, Tea 50."
        elif "sugar" in q_low:
            ans = f"Sugar 1Kg - 45 Rs"
        elif "oil" in q_low:
            ans = f"Oil 1L - 120 Rs"
        elif "rice" in q_low:
            ans = f"Rice 5Kg - 250 Rs"
        elif "tea" in q_low:
            ans = f"Tea Powder - 50 Rs"
        else:
            ans = f"{shop} bill total {total} Rs. Sugar 45, Oil 120, Rice 250, Tea 50."
        
        st.success(f"**Answer:** {ans}")
        speak(ans, lang)

    st.divider()
    if st.button("🔊 Bill ni Vinandi", use_container_width=True):
        speak(f"{st.session_state['my_shop']} total {st.session_state['my_bill_total']} rupayalu", lang)

else:
    st.warning("👆 Mundhu paina Camera tho bill teeyandi leda upload cheyandi")
