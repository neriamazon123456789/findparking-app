import streamlit as st
import time
import datetime

st.set_page_config(page_title="FindParking", page_icon="🅿️ FP", layout="centered")

# === שעה נוכחית
שעה_נוכחית = datetime.datetime.now().hour

# === ברכה
def קבל_ברכה():
    if שעה_נוכחית < 12:
        return "☀️! בוקר טוב"
    elif שעה_נוכחית < 17:
        return "🌤 ! צהריים טובים"
    else:
        return "🌙 ! ערב טוב"

# === רשימות כתובות לדוגמה
כתובות_שמותר_לחנות = [f"משה דיין {x} תל אביב" for x in [3,4,6,8,13,20,33,43]]
כתובות_כחול_לבן = [f"משה דיין {x} תל אביב" for x in
    [1,2,5,7,10,11,14,16,18,21,23,25,27,29,30,31,34,36,38,40,41,44,46,48,50,54,56,58,60]]
כתובות_חניה_אסורה = [f"משה דיין {x} תל אביב" for x in [15,17,19]]

# === אתחול מצב
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

# === עדכון שדה אם נבחרה כתובת מההיסטוריה
if st.session_state["כתובת_לבחירה"]:
    st.session_state["כתובת"] = st.session_state["כתובת_לבחירה"]
    st.session_state["כתובת_לבחירה"] = None

# === כותרת וברכה
st.markdown("<h1 style='text-align: center;'>🅿️ FP – FindParking</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center;'>{קבל_ברכה()}</h3>", unsafe_allow_html=True)

# === התראה אם עכשיו מחוץ לשעות חניה
if שעה_נוכחית < 8 or שעה_נוכחית >= 19:
    st.warning("⏰ שעות החניה הסתיימו (08:00–19:00). ייתכן שעכשיו אסור לחנות.")

st.info("🔍 הזן כתובת לבדיקה. לדוגמה: 'משה דיין 10 תל אביב'")

# === שדה כתובת
st.text_input(": הזן את הכתובת לבדיקה", key="כתובת")
if st.session_state["כתובת"]:
    כתובת = st.session_state["כתובת"]
    קישור_לוויז = f"https://waze.com/ul?q={כתובת.replace(' ', '%20')}&navigate=yes"
    st.markdown(f"[🔍 פתח בוויז]({קישור_לוויז})", unsafe_allow_html=True)


# === לחצן בדיקה
if st.button("📍 בדוק"):
    כתובת = st.session_state["כתובת"].strip().replace(",", "")
    אם_לא_בהיסטוריה = כתובת and כתובת not in st.session_state["היסטוריה"]
    if אם_לא_בהיסטוריה:
        st.session_state["היסטוריה"].insert(0, כתובת)

    אם_אסורה = any(כת in כתובת for כת in כתובות_חניה_אסורה)
    אם_כחול = any(כת in כתובת for כת in כתובות_כחול_לבן)
    אם_מותר = any(כת in כתובת for כת in כתובות_שמותר_לחנות)

    if אם_אסורה:
        st.error("🚫 אסור לחנות כאן.")
    elif אם_כחול:
        st.success("🔵 מותר לחנות כאן – חניה כחול־לבן")
        st.info("🕒 בין 8:00 ל־19:00")
    elif אם_מותר:
        st.success("✅ מותר לחנות כאן – חניה אפורה")
        st.info("🕒 בין 8:00 ל־19:00")
    else:
        st.warning("❓ אין מידע על הכתובת.")

# === היסטוריה + מועדפים
with st.expander("📜 היסטוריית כתובות + מועדפים"):
    הכל = st.session_state["מועדפים"] + [
        כת for כת in st.session_state["היסטוריה"] if כת not in st.session_state["מועדפים"]
    ]

    אם_יש = bool(הכל)
    if אם_יש:
        if st.button("🧹 נקה הכל"):
            st.session_state["היסטוריה"].clear()
            st.session_state["מועדפים"].clear()
            st.rerun()

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
# === שיתוף ואודות ===
st.markdown("---")
st.markdown("### 🔗 שתפו את האפליקציה עם חברים:")

קישור = "https://neriamazon123456789-findparking-app.streamlit.app"

st.code(קישור, language="markdown")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"[📲 שלח בוואטסאפ](https://wa.me/?text={קישור})", unsafe_allow_html=True)
with col2:
    st.markdown(f"[📩 שלח במייל](mailto:?subject=אפליקציית%20חניה%20מגניבה&body={קישור})", unsafe_allow_html=True)
with col3:
    st.markdown(f"[🌐 מעבר לאפליקציה]( {קישור} )", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### ℹ️ אודות")
st.markdown("""
אפליקציית **FindParking FP** אפליקנוצרה ככלי עזר לאיתור חניה ברחובות מסוימים בתל אביב
זוהי גרסת דמו ניסיונית לצורכי המחשה בלבד. אין לראות במידע תחליף לסימון בפועל   
כל הזכויות שמורות © 2025  
פותח על ידי [נריה מזון](https://github.com/neriamazon123456789)
""")
















