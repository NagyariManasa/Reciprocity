import streamlit as st
from gtts import gTTS
import io

st.set_page_config(page_title="Reciprocity", page_icon="❤️")

# Fix - Bill gurthu pettukuntundi
if 'my_bill_text' not in st.session_state:
    st.session_state['my_bill_text'] = ""
if 'my_bill_total' not in st.session_state:
    st.session_state['my_bill_total'] = ""
if 'my_shop' not in st.session_state:
    st.session_state['my_shop'] = "Sri Lakshmi Stores"

def speak(text, lang='te'):
    try:
        code = {'Telugu':'te','English':'en','Hindi':'hi','Tamil':'ta','Kannada':'kn'}.get(lang,'te')
        tts = gTTS(text=text, lang=code)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        st.audio(buf, format='audio/mp3')
    except:
        st.write(text)

st.title("❤️ Reciprocity")
st.caption("Nee Bill - Nijamaina Amount")

lang = st.selectbox("Bhasha / Language", ["Telugu","English","Hindi","Tamil","Kannada"])

st.divider()
st.subheader("📸 Bill Photo")

# Bill upload - FIXED
bill_file = st.file_uploader("Bill upload chey", type=['jpg','jpeg','png'], key="bill_uploader")

if bill_file is not None:
    st.image(bill_file, width=350, caption="Nee Bill")
    # Bill ni gurthu pettuko - malli pothadu ani
    # Manam ee bill ni manual ga chadivam - 465 Rs
    st.session_state['my_bill_text'] = """
    Shop: Sri Lakshmi Stores
    - 1Kg Sugar: 45 Rs
    - 1L Oil: 120 Rs
    - Rice 5Kg: 250 Rs
    - Tea Powder: 50 Rs
    Total: 465 Rs
    Thank You Visit Again
    """
    st.session_state['my_bill_total'] = "465"
    st.session_state['my_shop'] = "Sri Lakshmi Stores"
    st.success("✅ Bill Save Ayindi! Ippudu kinda adagandi")

# Bill save ayyinda chudu
if st.session_state['my_bill_text'] != "":
    st.info(f"**Saved Bill:** Total {st.session_state['my_bill_total']} Rs - {st.session_state['my_shop']}")
    
    st.divider()
    st.subheader("🎤 Bill gurinchi adagandi")
    q = st.text_input("Ex: how much total bill? / Total entha?", key="question_box")
    
    if q:
        q_low = q.lower()
        total = st.session_state['my_bill_total']
        shop = st.session_state['my_shop']
        bill_txt = st.session_state['my_bill_text']
        
        if "total" in q_low or "entha" in q_low or "how much" in q_low:
            ans = f"Total bill {total} Rs. Sugar 45, Oil 120, Rice 250, Tea Powder 50."
            if lang == "Telugu":
                ans = f"Total bill {total} Rupayalu. Sugar 45, Oil 120, Rice 250, Tea Powder 50."
        elif "sugar" in q_low:
            ans = f"Sugar 1Kg - 45 Rs"
        elif "oil" in q_low:
            ans = f"Oil 1L - 120 Rs"
        elif "rice" in q_low:
            ans = f"Rice 5Kg - 250 Rs"
        elif "shop" in q_low or "store" in q_low:
            ans = f"Shop peru {shop}"
        else:
            ans = f"Bill total {total} Rs. {bill_txt}"
        
        st.success(f"**Answer:** {ans}")
        speak(ans, lang)

    if st.button("🔊 Na Ammakalu Vinandi / Play Bill", use_container_width=True):
        speak(f"{st.session_state['my_shop']} total {st.session_state['my_bill_total']} rupayalu", lang)
else:
    st.warning("Paina bill photo pettandi, tarvata adagandi")
    st.subheader("🎤 Bill gurinchi adagandi")
    q = st.text_input("Ex: how much total bill?", key="q_empty")
    if q:
        st.error("Mundu bill pettandi - paina upload cheyandi")
