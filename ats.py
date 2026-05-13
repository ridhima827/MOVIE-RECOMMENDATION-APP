import streamlit as st
import pdfplumber
import re
import pandas as pd
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="AI ATS Resume Scanner",
    page_icon="🚀",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#0f172a,#1e293b,#111827);
    color:white;
}

/* Title */
.main-title{
    text-align:center;
    font-size:60px;
    font-weight:bold;
    color:white;
    margin-top:10px;
}

.sub-title{
    text-align:center;
    color:#cbd5e1;
    font-size:20px;
    margin-bottom:30px;
}

/* Cards */
.card{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    border-radius:20px;
    padding:25px;
    box-shadow:0px 8px 30px rgba(0,0,0,0.3);
    margin-bottom:20px;
}

/* Skill tags */
.skill{
    display:inline-block;
    padding:8px 14px;
    margin:6px;
    border-radius:20px;
    background:linear-gradient(to right,#38bdf8,#6366f1);
    color:white;
    font-weight:bold;
    font-size:14px;
}

/* Score box */
.score-box{
    text-align:center;
    padding:35px;
    border-radius:25px;
    background:linear-gradient(to right,#06b6d4,#3b82f6);
    color:white;
    font-size:35px;
    font-weight:bold;
    box-shadow:0px 6px 20px rgba(0,0,0,0.4);
}

/* Metrics */
.metric-box{
    background: rgba(255,255,255,0.08);
    padding:20px;
    border-radius:20px;
    text-align:center;
    box-shadow:0px 4px 20px rgba(0,0,0,0.2);
}

/* Footer */
.footer{
    text-align:center;
    color:#cbd5e1;
    padding:20px;
    font-size:16px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown(
    '<div class="main-title">🚀 AI ATS Resume Scanner</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Smart Resume Analysis • ATS Matching • Skill Detection • AI Suggestions</div>',
    unsafe_allow_html=True
)

# =========================================================
# SKILLS DATABASE
# =========================================================
skills_db = [
    "python","java","c","c++","html","css","javascript",
    "sql","mysql","mongodb","machine learning","deep learning",
    "data analytics","power bi","tableau","excel","pandas",
    "numpy","streamlit","flask","django","react","node js",
    "git","github","aws","azure","nlp","tensorflow","opencv",
    "artificial intelligence","data science","communication",
    "problem solving","teamwork","leadership","fastapi",
    "ui ux","figma","linux","cloud computing"
]

# =========================================================
# FUNCTIONS
# =========================================================
def extract_text_from_pdf(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + " "

    return text.lower()


def extract_skills(text):

    found_skills = []

    for skill in skills_db:

        pattern = r"\\b" + re.escape(skill) + r"\\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return list(set(found_skills))


def calculate_ats_score(resume_skills, jd_skills):

    matched = list(set(resume_skills) & set(jd_skills))

    if len(jd_skills) == 0:
        return 0, matched

    score = (len(matched) / len(jd_skills)) * 100

    return round(score,2), matched


def generate_feedback(score):

    if score >= 80:
        return "Excellent Resume Match ✅"

    elif score >= 60:
        return "Good Resume But Needs Improvement ⚡"

    elif score >= 40:
        return "Average Match — Add More Skills 📈"

    else:
        return "Low ATS Match — Improve Resume 🚨"

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        width=120
    )

    st.header("📌 Features")

    st.write("✅ ATS Score")
    st.write("✅ Resume Skill Detection")
    st.write("✅ Missing Skills")
    st.write("✅ AI Suggestions")
    st.write("✅ Resume Statistics")
    st.write("✅ Skill Matching")
    st.write("✅ Smart UI Dashboard")

    st.markdown("---")

    st.subheader("👨‍💻 Developer Info")

    st.write("Project using:")
    st.write("- Streamlit")
    st.write("- NLP")
    st.write("- PDF Processing")
    st.write("- Regex Matching")

# =========================================================
# INPUT SECTION
# =========================================================
left,right = st.columns(2)

with left:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "📄 Upload Resume PDF",
        type=["pdf"]
    )

    st.markdown('</div>', unsafe_allow_html=True)

with right:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    job_description = st.text_area(
        "📝 Paste Job Description",
        height=250
    )

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ANALYZE BUTTON
# =========================================================
analyze = st.button("🚀 Analyze Resume")

# =========================================================
# MAIN PROCESS
# =========================================================
if analyze:

    if uploaded_file is not None and job_description != "":

        # Extract text
        resume_text = extract_text_from_pdf(uploaded_file)

        # Skills
        resume_skills = extract_skills(resume_text)

        jd_skills = extract_skills(job_description.lower())

        # ATS Score
        ats_score, matched_skills = calculate_ats_score(
            resume_skills,
            jd_skills
        )

        # Missing Skills
        missing_skills = list(
            set(jd_skills) - set(resume_skills)
        )

        # Feedback
        feedback = generate_feedback(ats_score)

        # =========================================================
        # SCORE SECTION
        # =========================================================
        st.markdown(
            f"""
            <div class="score-box">
                ATS MATCH SCORE <br><br>
                {ats_score}%<br><br>
                <div style='font-size:22px'>
                {feedback}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")
        st.progress(int(ats_score))

        # =========================================================
        # METRICS
        # =========================================================
        m1,m2,m3,m4 = st.columns(4)

        with m1:
            st.markdown(
                f"""
                <div class="metric-box">
                <h2>{len(resume_skills)}</h2>
                Resume Skills
                </div>
                """,
                unsafe_allow_html=True
            )

        with m2:
            st.markdown(
                f"""
                <div class="metric-box">
                <h2>{len(jd_skills)}</h2>
                JD Skills
                </div>
                """,
                unsafe_allow_html=True
            )

        with m3:
            st.markdown(
                f"""
                <div class="metric-box">
                <h2>{len(matched_skills)}</h2>
                Matched
                </div>
                """,
                unsafe_allow_html=True
            )

        with m4:
            st.markdown(
                f"""
                <div class="metric-box">
                <h2>{len(missing_skills)}</h2>
                Missing
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")

        # =========================================================
        # RESULTS SECTION
        # =========================================================
        c1,c2,c3 = st.columns(3)

        # Resume Skills
        with c1:

            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.subheader("📌 Resume Skills")

            if resume_skills:

                for skill in resume_skills:
                    st.markdown(
                        f'<span class="skill">{skill}</span>',
                        unsafe_allow_html=True
                    )

            else:
                st.warning("No skills found")

            st.markdown('</div>', unsafe_allow_html=True)

        # Matched Skills
        with c2:

            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.subheader("✅ Matched Skills")

            if matched_skills:

                for skill in matched_skills:
                    st.markdown(
                        f'<span class="skill">{skill}</span>',
                        unsafe_allow_html=True
                    )

            else:
                st.warning("No matched skills")

            st.markdown('</div>', unsafe_allow_html=True)

        # Missing Skills
        with c3:

            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.subheader("❌ Missing Skills")

            if missing_skills:

                for skill in missing_skills:
                    st.markdown(
                        f'<span class="skill">{skill}</span>',
                        unsafe_allow_html=True
                    )

            else:
                st.success("No missing skills")

            st.markdown('</div>', unsafe_allow_html=True)

        # =========================================================
        # AI SUGGESTIONS
        # =========================================================
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("🤖 AI Resume Suggestions")

        if ats_score >= 80:
            st.success(
                "Your resume is highly optimized for ATS systems."
            )

        elif ats_score >= 60:
            st.info(
                "Add more technical keywords and project details."
            )

        elif ats_score >= 40:
            st.warning(
                "Include missing tools, technologies, and certifications."
            )

        else:
            st.error(
                "Resume needs significant improvement for ATS filtering."
            )

        st.markdown('</div>', unsafe_allow_html=True)

        # =========================================================
        # RESUME STATISTICS
        # =========================================================
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("📊 Resume Statistics")

        word_count = len(resume_text.split())

        char_count = len(resume_text)

        stats = pd.DataFrame({
            "Metric": [
                "Words",
                "Characters",
                "Resume Skills",
                "Matched Skills",
                "Missing Skills"
            ],
            "Value": [
                word_count,
                char_count,
                len(resume_skills),
                len(matched_skills),
                len(missing_skills)
            ]
        })

        st.dataframe(stats, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # =========================================================
        # DOWNLOAD REPORT
        # =========================================================
        report = f"""
AI ATS Resume Scanner Report
Generated on: {datetime.now()}

ATS Score: {ats_score}%

Resume Skills:
{', '.join(resume_skills)}

Matched Skills:
{', '.join(matched_skills)}

Missing Skills:
{', '.join(missing_skills)}

Feedback:
{feedback}
"""

        st.download_button(
            label="📥 Download ATS Report",
            data=report,
            file_name="ATS_Report.txt",
            mime="text/plain"
        )

    else:
        st.error("Please upload resume and enter job description.")

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")

st.markdown(
    '<div class="footer">🚀 Built using Streamlit • NLP • AI • PDF Processing</div>',
    unsafe_allow_html=True
)