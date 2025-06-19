import streamlit as st
import time
import datetime

st.set_page_config(page_title="FindParking", page_icon="🅿️ FP", layout="centered")

שעה_נוכחית = datetime.datetime.now().hour

def קבל_ברכה():
    if שעה_נוכחית < 12:
        return "☀️! בוקר טוב"
    elif שעה_נוכחית < 17:
        return "🌤 ! צהריים טובים"
    else:
        return "🌙 ! ערב טוב"

def תקן_עיר_בכתובת(כתובת):
    כתובת = כתובת.strip().replace("  ", " ")
    כתובת = כתובת.replace("תל אביב-יפו", "תל אביב")
    כתובת = כתובת.replace("יפו", "תל אביב")
    while "תל אביב תל אביב" in כתובת:
        כתובת = כתובת.replace("תל אביב תל אביב", "תל אביב")
    return כתובת

כתובות_שמותר_לחנות = [f"משה דיין {x} תל אביב" for x in [3,4,6,8,9,12,13,20,33]]
כתובות_כחול_לבן = [f"משה דיין {x} תל אביב" for x in range(1, 86) if x not in [3,4,6,8,9,12,13,15,17,19,20,33]]
כתובות_חניה_אסורה = [f"משה דיין {x} תל אביב" for x in [15,17,19]]

כתובות_שמותר_לחנות += [f"רבי טרפון {x} תל אביב" for x in [1, 3, 5]]
כתובות_כחול_לבן += [f"רבי טרפון {x} תל אביב" for x in [2, 4, 6, 7, 49]]
כתובות_חניה_אסורה += [f"רבי טרפון {x} תל אביב" for x in [9]]

# אתחול session_state
if "טיימר_פעיל" not in st.session_state:
    st.session_state["טיימר_פעיל"] = False
if "זמן_שניות" not in st.session_state:
    st.session_state["זמן_שניות"] = 0
for key in ["כתובת", "היסטוריה", "מועדפים", "כתובת_לבחירה"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key == "כתובת" else [] if key in ["היסטוריה", "מועדפים"] else None

if st.session_state["כתובת_לבחירה"]:
    st.session_state["כתובת"] = st.session_state["כתובת_לבחירה"]
    st.session_state["כתובת_לבחירה"] = None

st.markdown("<h1 style='text-align: center;'>🅿️ FP – FindParking</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center;'>{קבל_ברכה()}</h3>", unsafe_allow_html=True)

if שעה_נוכחית < 8 or שעה_נוכחית >= 19:
    st.warning("⏰ שעות החניה הסתיימו (08:00–19:00). ייתכן שעכשיו אסור לחנות.")


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

# ⏱️ מנגנון טיימר עם הגנה מפני כפילות
if st.session_state["טיימר_פעיל"] and "הורץ_פעם_אחת" not in st.session_state:
    st.session_state["הורץ_פעם_אחת"] = True
    time.sleep(1)
    st.session_state["זמן_שניות"] += 1
    del st.session_state["הורץ_פעם_אחת"]
    st.rerun()

st.markdown("---")
st.markdown("### 🔗 שתפו את האפליקציה עם חברים:")

קישור = "https://neriamazon123456789-findparking-app.streamlit.app"
st.code(קישור, language="markdown")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"[📲 שלח בוואטסאפ](https://wa.me/?text=מצאתי%20אפליקציה%20למצוא%20חניה!%20{קישור})", unsafe_allow_html=True)
with col2:
    st.markdown(f"[📩 שלח במייל](mailto:?subject=מצאתי%20אפליקציית%20חניה&body={קישור})", unsafe_allow_html=True)
with col3:
    st.markdown(f"[🌐 מעבר לאפליקציה]({קישור})", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### ℹ️ אודות")
st.markdown("""
אפליקציית **FindParking FP** פותחה ככלי עזר לאיתור חניה ברחובות מסוימים בתל אביב  
🚧 *זוהי גרסת דמו ניסיונית לצורכי המחשה בלבד*  
🛑 *אין לראות במידע תחליף לתמרורים בפועל*  

כל הזכויות שמורות © 2025  
פותח על ידי [נריה מזון](https://github.com/neriamazon123456789)
""")




















