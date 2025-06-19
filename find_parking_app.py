import streamlit as st
import time
import datetime
import urllib.parse

st.set_page_config(page_title="FindParking", page_icon="🅿️ FP", layout="centered")

# ⏰ זמן נוכחי
עכשיו = datetime.datetime.now()
שעה = עכשיו.hour
דקה = עכשיו.minute
תאריך_היום = עכשיו.date()

# 🪪 אתחול משתני מצב
if "טיימר_פעיל" not in st.session_state:
    st.session_state["טיימר_פעיל"] = False
if "זמן_שניות" not in st.session_state:
    st.session_state["זמן_שניות"] = 0
if "כתובת" not in st.session_state:
    st.session_state["כתובת"] = ""
if "כתובת_לבחירה" not in st.session_state:
    st.session_state["כתובת_לבחירה"] = None
if "היסטוריה" not in st.session_state:
    st.session_state["היסטוריה"] = []
if "מועדפים" not in st.session_state:
    st.session_state["מועדפים"] = []
if "רוצה_תזכורת" not in st.session_state:
    st.session_state["רוצה_תזכורת"] = False
if "ביקש_תזכורת" not in st.session_state:
    st.session_state["ביקש_תזכורת"] = False
if "התראה_18_30" not in st.session_state or st.session_state.get("תאריך_התראה") != תאריך_היום:
    st.session_state["התראה_18_30"] = False
    st.session_state["תאריך_התראה"] = תאריך_היום

# ⛔️ בסיס כתובות (דוגמה דמו)
כתובות_שמותר_לחנות = [f"משה דיין {x} תל אביב" for x in [3,4,6,8,9,12,13,20,33]]
כתובות_כחול_לבן = [f"משה דיין {x} תל אביב" for x in range(1,86) if x not in [3,4,6,8,9,12,13,15,17,19,20,33]]
כתובות_חניה_אסורה = [f"משה דיין {x} תל אביב" for x in [15,17,19]]
כתובות_שמותר_לחנות += [f"רבי טרפון {x} תל אביב" for x in [1,3,5]]
כתובות_כחול_לבן += [f"רבי טרפון {x} תל אביב" for x in [2,4,6,7,49]]
כתובות_חניה_אסורה += [f"רבי טרפון {x} תל אביב" for x in [9]]

# 👋 ברכה
def קבל_ברכה():
    if שעה < 12:
        return "☀️ בוקר טוב"
    elif שעה < 17:
        return "🌤 צהריים טובים"
    else:
        return "🌙 ערב טוב"

st.markdown(f"# 🅿️ FP – FindParking\n### {קבל_ברכה()}", unsafe_allow_html=True)

if שעה < 8 or שעה >= 19:
    st.warning("⏰ שעות החניה הסתיימו (08:00–19:00). ייתכן שעכשיו אסור לחנות.")

# 🧼 תיקן עיר
def תקן_עיר_בכתובת(כתובת):
    כתובת = כתובת.strip().replace("  ", " ")
    כתובת = כתובת.replace("תל אביב-יפו", "תל אביב").replace("יפו", "תל אביב")
    while "תל אביב תל אביב" in כתובת:
        כתובת = כתובת.replace("תל אביב תל אביב", "תל אביב")
    return כתובת

# 📥 קלט כתובת
st.text_input("🔍 הזן כתובת לבדיקה", key="כתובת")

# 🛎️ כפתור להפעיל תזכורת
if st.button("🔔 הפעל תזכורת ל־18:30 להזיז את הרכב"):
    st.session_state["רוצה_תזכורת"] = True
    st.success("🔔 תזכורת הופעלה! נודיע לך ב־18:30 אם בדקת כתובת בתל אביב")

# 📍 בדיקת כתובת
if st.button("📍 בדוק"):
    כתובת = תקן_עיר_בכתובת(st.session_state["כתובת"]).replace(",", "")
    st.success(f"בוצעה בדיקה על: {כתובת}")

    # 🔐 זיהוי לצורך תזכורת
    אם_בת_א = "תל אביב" in כתובת
    אם_רוצה = st.session_state["רוצה_תזכורת"]
    if אם_רוצה and אם_בת_א:
        st.session_state["ביקש_תזכורת"] = True

    # היסטוריה
    אם_לא_בהיסטוריה = כתובת and כתובת not in st.session_state["היסטוריה"]
    if אם_לא_בהיסטוריה:
        st.session_state["היסטוריה"].insert(0, כתובת)

    # תוצאה
    אם_אסורה = any(כת in כתובת for כת in כתובות_חניה_אסורה)
    אם_כחול = any(כת in כתובת for כת in כתובות_כחול_לבן)
    אם_מותר = any(כת in כתובת for כת in כתובות_שמותר_לחנות)

    if אם_אסורה:
        st.error("🚫 אסור לחנות כאן.")
    elif אם_כחול:
        st.success("🔵 מותר לחנות כאן – חניה כחול־לבן")
    elif אם_מותר:
        st.success("✅ מותר לחנות כאן – חניה אפורה")
    else:
        st.warning("❓ אין מידע על הכתובת.")

# 🛎️ הצגת ההתראה ב־18:30 אם התקיימו התנאים
if (
    st.session_state["ביקש_תזכורת"] and
    שעה == 18 and דקה == 30 and
    not st.session_state["התראה_18_30"]
):
    st.warning("⏰ עוד חצי שעה מסתיימת החניה (19:00)! אל תשכח להזיז את הרכב 🚗")
    st.session_state["התראה_18_30"] = True

# 🕒 טיימר
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

    כתובת = תקן_עיר_בכתובת(st.session_state["כתובת"]).replace(",", "")
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

    st.session_state["טיימר_פעיל"] = מצב_לפני
    st.session_state["זמן_שניות"] = שניות_לפני

with st.expander("📜 היסטוריית כתובות + מועדפים"):
    הכל = st.session_state["מועדפים"] + [כת for כת in st.session_state["היסטוריה"] if כת not in st.session_state["מועדפים"]]
    if הכל:
        if st.button("🧹 נקה הכל"):
            st.session_state["היסטוריה"].clear()
            st.session_state["מועדפים"].clear()
            st.rerun()
        for i, כתובת_עבר in enumerate(הכל):
            שורה = st.columns([6,1])
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

# ✅ טיימר שעובד תמיד
st.markdown("---")
st.markdown("### ⏱️ טיימר חניה")

ש = st.session_state["זמן_שניות"] // 3600
ד = (st.session_state["זמן_שניות"] % 3600) // 60
שנ = st.session_state["זמן_שניות"] % 60
st.markdown(f"## 🕒 {ש:02}:{ד:02}:{שנ:02}")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🟢 התחל", key="התחל"):
        st.session_state["טיימר_פעיל"] = True
with col2:
    if st.button("⏸ הפסק", key="הפסק"):
        st.session_state["טיימר_פעיל"] = False
with col3:
    if st.button("🔁 איפוס", key="איפוס"):
        st.session_state["טיימר_פעיל"] = False
        st.session_state["זמן_שניות"] = 0

# מנגנון טיימר – בלולאה שמחזיקה גם אחרי בדיקה
if st.session_state["טיימר_פעיל"] and "הורץ_פעם_אחת" not in st.session_state:
    st.session_state["הורץ_פעם_אחת"] = True
    time.sleep(1)
    st.session_state["זמן_שניות"] += 1
    del st.session_state["הורץ_פעם_אחת"]
    st.rerun()
# 🔗 שיתוף
st.markdown("---")
st.markdown("### 🔗 שתפו את האפליקציה עם חברים:")

קישור = "https://neriamazon123456789-findparking-app.streamlit.app"
st.code(קישור, language="markdown")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        f"[📲 שלח בוואטסאפ](https://wa.me/?text=מצאתי%20אפליקציה%20למצוא%20חניה!%20{קישור})",
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        f"[📩 שלח במייל](mailto:?subject=מצאתי%20אפליקציית%20חניה&body={קישור})",
        unsafe_allow_html=True
    )
with col3:
    st.markdown(f"[🌐 מעבר לאפליקציה]({קישור})", unsafe_allow_html=True)
st.markdown("---")
st.markdown("### 💬 משוב")

st.markdown(
    "[📝 לחץ כאן כדי לתת לנו משוב על האפליקציה](https://forms.gle/QYEdwmEFyEogMnEn9)",
    unsafe_allow_html=True
)

# ℹ️ אודות
st.markdown("---")
st.markdown("### ℹ️ אודות")
st.markdown("""
אפליקציית **FindParking FP** פותחה ככלי עזר לאיתור חניה ברחובות מסוימים בתל אביב  
🚧 *זוהי גרסת דמו ניסיונית לצורכי המחשה בלבד*  
🛑 *אין לראות במידע תחליף לתמרורים בפועל*  

כל הזכויות שמורות © 2025  
פותח על ידי [נריה מזון](https://github.com/neriamazon123456789)
""")





























