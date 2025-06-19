
import streamlit as st
import time
import datetime
import urllib.parse

st.set_page_config(page_title="FindParking", page_icon="🅿️ FP", layout="centered")

# אתחול משתני טיימר
if "טיימר_פעיל" not in st.session_state:
    st.session_state["טיימר_פעיל"] = False
if "זמן_שניות" not in st.session_state:
    st.session_state["זמן_שניות"] = 0

# לולאת הטיימר שעובדת תמידית
if st.session_state["טיימר_פעיל"]:
    time.sleep(1)
    st.session_state["זמן_שניות"] += 1
    st.rerun()

# ברכה
שעה = datetime.datetime.now().hour
ברכה = "☀️ בוקר טוב" if שעה < 12 else "🌤 צהריים טובים" if שעה < 17 else "🌙 ערב טוב"
st.markdown(f"# 🅿️ FP – FindParking\n### {ברכה}")

# קלט כתובת
כתובת = st.text_input("🔍 הזן כתובת לבדיקה")
if כתובת:
    כתובת_לשליחה = urllib.parse.quote(כתובת)
    קישור_לוויז = f"https://waze.com/ul?q={כתובת_לשליחה}&navigate=yes"
    st.markdown(f"[🚗 פתח בוויז ל־{כתובת}]({קישור_לוויז})", unsafe_allow_html=True)

# כפתור בדיקה
if st.button("📍 בדוק"):
    מצב_טיימר = st.session_state["טיימר_פעיל"]
    שניות = st.session_state["זמן_שניות"]
    st.success("✅ כתובת נבדקה! (הדמו אינו בודק בפועל)")
    st.session_state["טיימר_פעיל"] = מצב_טיימר
    st.session_state["זמן_שניות"] = שניות

# טיימר מוצג
st.markdown("---\n### ⏱️ טיימר חניה")
ש = st.session_state["זמן_שניות"] // 3600
ד = (st.session_state["זמן_שניות"] % 3600) // 60
שנ = st.session_state["זמן_שניות"] % 60
st.markdown(f"## 🕒 {ש:02}:{ד:02}:{שנ:02}")

# כפתורי שליטה בטיימר
col1, col2, col3 = st.columns(3)
with col1:
    if st.session_state["טיימר_פעיל"]:
        if st.button("⏸ הפסק", key="הפסק"):
            st.session_state["טיימר_פעיל"] = False
    else:
        if st.session_state["זמן_שניות"] == 0:
            if st.button("🟢 התחל", key="התחל"):
                st.session_state["טיימר_פעיל"] = True
        else:
            if st.button("▶️ המשך", key="המשך"):
                st.session_state["טיימר_פעיל"] = True
with col2:
    if st.button("🔁 איפוס", key="איפוס"):
        st.session_state["טיימר_פעיל"] = False
        st.session_state["זמן_שניות"] = 0

# שתף
st.markdown("---\n### 📲 שיתוף האפליקציה")
קישור = "https://neriamazon123456789-findparking-app.streamlit.app"
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"[📲 שלח בוואטסאפ](https://wa.me/?text=מצאתי%20אפליקציה%20למצוא%20חניה!%20{קישור})", unsafe_allow_html=True)
with col2:
    st.markdown(f"[📩 שלח במייל](mailto:?subject=מצאתי%20אפליקציית%20חניה&body={קישור})", unsafe_allow_html=True)
with col3:
    st.markdown(f"[🌐 צפה באפליקציה]({קישור})", unsafe_allow_html=True)

# משוב
st.markdown("---\n### 💬 משוב")
st.markdown("[📝 לחץ כאן כדי לתת משוב על האפליקציה](https://forms.gle/your-google-form-link)", unsafe_allow_html=True)

# אודות
st.markdown("---\n### ℹ️ אודות")
st.markdown("""
אפליקציית **FindParking FP** נבנתה כדי לעזור לך להבין איפה מותר לחנות בתל אביב  
🚧 גרסת דמו בלבד  
🛑 אין לראות בזה תחליף לתמרור פיזי בפועל  

פותח באהבה ❤️ על ידי נריה מזון  
[🔗 github.com/neriamazon123456789](https://github.com/neriamazon123456789)
""")
























