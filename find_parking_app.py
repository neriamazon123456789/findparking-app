import streamlit as st
import time
import datetime

st.set_page_config(page_title="FindParking", page_icon="🅿️", layout="centered")

# === ברכה לפי שעה ===
def קבל_ברכה():
    שעה = datetime.datetime.now().hour
    if שעה < 12:
        return "☀️ בוקר טוב!"
    elif שעה < 17:
        return "🌤 צהריים טובים!"
    else:
        return "🌙 ערב טוב!"

# === מאגרי כתובות
כתובות_שמותר_לחנות = [f"משה דיין {x} תל אביב" for x in [3,4,6,8,13,20,33,43]]
כתובות_כחול_לבן = [f"משה דיין {x} תל אביב" for x in [1,2,5,7,10,11,14,16,18,21,23,25,27,29,30,31,
    34,36,38,40,41,44,46,48,50,54,56,58,60]]
כתובות_חניה_אסורה = [f"משה דיין {x} תל אביב" for x in [100,101]]

# === אתחול session_state
ברירת_מחדל = {
    "כתובת": "",
    "היסטוריה": [],
    "מועדפים": [],
    "כתובת_לבחירה": None,
    "טיימר_פעיל": False,
    "זמן_שניות": 0
}
for key, val in ברירת_מחדל.items():
    if key not in st.session_state:
        st.session_state[key] = val

# === אם נבחרה כתובת מהיסטוריה – הכנס לשדה
if st.session_state["כתובת_לבחירה"]:
    st.session_state["כתובת"] = st.session_state["כתובת_לבחירה"]
    st.session_state["כתובת_לבחירה"] = None

# === כותרת וברכה
st.markdown("<h1 style='text-align: center;'>🅿️ FindParking</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center;'>{קבל_ברכה()}</h3>", unsafe_allow_html=True)
st.info("🔍 הזן כתובת לבדיקה. לדוגמה: 'משה דיין 10 תל אביב'")

# === שדה כתובת
st.text_input("כתובת לבדיקה:", key="כתובת")

# === כפתור בדיקה
if st.button("📍 בדוק"):
    כתובת = st.session_state["כתובת"].strip().replace(",", "")
    if not כתובת:
        st.warning("⚠️ אנא הזן כתובת.")
    else:
        אם_לא_בהיסטוריה = כתובת not in st.session_state["היסטוריה"]
        if אם_לא_בהיסטוריה:
            st.session_state["היסטוריה"].insert(0, כתובת)

        אם_אסורה = any(כת in כתובת for כת in כתובות_חניה_אסורה)
        אם_כחול = any(כת in כתובת for כת in כתובות_כחול_לבן)
        אם_מותר = any(כת in כתובת for כת in כתובות_שמותר_לחנות)

        if אם_אסורה:
            st.error("🚫 אסור לחנות כאן.")
        elif אם_כחול:
            st.success("🔵 מותר לחנות כאן – חניה כחול־לבן")
            st.info("🕒 מותרת בין 8:00 ל־19:00")
        elif אם_מותר:
            st.success("✅ מותר לחנות כאן – חניה אפורה")
            st.info("🕒 מותרת בין 8:00 ל־19:00")
        else:
            st.warning("❓ אין מידע על הכתובת.")

# === היסטוריה + מועדפים
with st.expander("📜 היסטוריית כתובות + מועדפים"):
    אם_יש_משהו = st.session_state["היסטוריה"] or st.session_state["מועדפים"]

    if אם_יש_משהו:
        הכל = st.session_state["מועדפים"] + [
            כת for כת in st.session_state["היסטוריה"] if כת not in st.session_state["מועדפים"]
        ]

        for i, כתובת_עבר in enumerate(הכל):
            שורה = st.columns([6, 1])
            עם_כוכב = כתובת_עבר in st.session_state["מועדפים"]

            with שורה[0]:
                if st.button(f"{'⭐ ' if עם_כוכב else ''}{כתובת_עבר}", key=f"היסטוריה_{i}"):
                    st.session_state["כתובת_לבחירה"] = כתובת_עבר
                    st.rerun()

            with שורה[1]:
                if st.button("★" if עם_כוכב else "☆", key=f"כוכב_{i}"):
                    if עם_כוכב:
                        st.session_state["מועדפים"].remove(כתובת_עבר)
                    else:
                        st.session_state["מועדפים"].insert(0, כתובת_עבר)
                    st.rerun()
    else:
        st.markdown("_אין עדיין היסטוריה להצגה._")

# === טיימר חניה
st.markdown("---")
st.markdown("### ⏱️ טיימר חניה")

ש = st.session_state["זמן_שניות"] // 3600
ד = (st.session_state["זמן_שניות"] % 3600) // 60
שנ = st.session_state["זמן_שניות"] % 60
st.markdown(f"## 🕒 {ש:02}:{ד:02}:{שנ:02}")

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

if st.session_state["טיימר_פעיל"]:
    time.sleep(1)
    st.session_state["זמן_שניות"] += 1
    st.rerun()














