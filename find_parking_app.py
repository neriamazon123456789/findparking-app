import streamlit as st
import datetime
import time


st.set_page_config(page_title="FindParking", page_icon="🅿️", layout="centered")

# === פונקציית ברכה לפי שעה ===
def קבל_ברכה():
    שעה = datetime.datetime.now().hour
    if שעה < 12:
        return "☀️ בוקר טוב!"
    elif שעה < 17:
        return "🌤 צהריים טובים!"
    else:
        return "🌙 ערב טוב!"

# === כתובות לדוגמה ===
כתובות_שמותר_לחנות = [f"משה דיין {x} תל אביב" for x in [3, 4, 6, 8, 13, 20, 33, 43]]
כתובות_כחול_לבן = [f"משה דיין {x} תל אביב" for x in [1,2,5,7,10,11,14,16,18,21,23,25,27,29,30,31,34,36,38,40,41,44,46,48,50,54,56,58,60]]
כתובות_חניה_אסורה = [f"משה דיין {x} תל אביב" for x in [100, 101]]

# === אתחול session_state ===
for key, val in {
    "כתובת": "",
    "היסטוריה": [],
    "כתובת_לבחירה": None,
    "טיימר_פעיל": False,
    "זמן_שניות": 0
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# === הכנסת כתובת מהיסטוריה (אם נבחרה) ===
if st.session_state["כתובת_לבחירה"]:
    st.session_state["כתובת"] = st.session_state["כתובת_לבחירה"]
    st.session_state["כתובת_לבחירה"] = None

# === כותרת וברכה ===
st.markdown("<h1 style='text-align: center;'>🅿️ FindParking</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center;'>{קבל_ברכה()}</h3>", unsafe_allow_html=True)
st.info("🔍 הזן כתובת לבדיקה. למשל: 'משה דיין 10 תל אביב'")

# === שדה כתובת לבדיקה ===
st.text_input("כתובת לבדיקה:", key="כתובת")

if st.button("📍 בדוק"):
    כתובת = st.session_state["כתובת"].strip().replace(",", "")
    if not כתובת:
        st.warning("⚠️ נא להזין כתובת.")
    else:
        if כתובת not in st.session_state["היסטוריה"]:
            st.session_state["היסטוריה"].insert(0, כתובת)

        אם_אסורה = any(כת in כתובת for כת in כתובות_חניה_אסורה)
        אם_כחול = any(כת in כתובת for כת in כתובות_כחול_לבן)
        אם_מותר = any(כת in כתובת for כת in כתובות_שמותר_לחנות)

        if אם_אסורה:
            st.error("🚫 אסור לחנות כאן בכלל.")
        elif אם_כחול:
            st.success("🔵 מותר לחנות כאן – חניה כחול־לבן")
            st.info("🕒 מותרת בין 8:00 ל־19:00")
        elif אם_מותר:
            st.success("✅ מותר לחנות כאן – חניה אפורה")
            st.info("🕒 מותרת בין 8:00 ל־19:00")
        else:
            st.warning("❓ אין מידע על הכתובת.")

# === היסטוריית חיפושים ===
with st.expander("📜 היסטוריית כתובות"):
    if st.session_state["היסטוריה"]:
        for i, כתובת_עבר in enumerate(st.session_state["היסטוריה"]):
            if st.button(כתובת_עבר, key=f"היסטוריה_{i}"):
                st.session_state["כתובת_לבחירה"] = כתובת_עבר
                st.rerun()
    else:
        st.markdown("_לא קיימת היסטוריה כרגע._")

# === טיימר חניה ===
st.markdown("---")
st.markdown("### ⏱️ טיימר חניה")

שעות = st.session_state["זמן_שניות"] // 3600
דקות = (st.session_state["זמן_שניות"] % 3600) // 60
שניות = st.session_state["זמן_שניות"] % 60
st.markdown(f"## 🕒 {שעות:02}:{דקות:02}:{שניות:02}")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🟢 התחל"):
        st.session_state["טיימר_פעיל"] = True
with col2:
    if st.button("⏸ הפסק"):
        st.session_state["טיימר_פעיל"] = False
with col3:
    if st.button("🔁 איפוס"):
        st.session_state["טיימר_פעיל"] = False
        st.session_state["זמן_שניות"] = 0

# רענון כל שנייה בזמן שהטיימר פעיל
if st.session_state["טיימר_פעיל"]:
       time.sleep(1)

    st.session_state["זמן_שניות"] += 1
    st.rerun()












