"""
app.py
------
Main Streamlit application interface for AI Resume Analyzer.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Custom modules
import resume_parser
import skills
import analyzer
import report_generator


# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Custom CSS styling
st.markdown("""
<style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    
    /* Header banner styling */
    .header-banner {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .header-banner h1 {
        color: #f8fafc;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    .header-banner p {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 0;
    }

    /* Metric card styling */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.25rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-card .value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0f172a;
    }
    .metric-card .label {
        font-size: 0.9rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Score gauge box */
    .score-container {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }

    /* Skill tags/badges styling */
    .tag-matched {
        display: inline-block;
        background-color: #dcfce7;
        color: #166534;
        border: 1px solid #bbf7d0;
        padding: 4px 10px;
        border-radius: 16px;
        font-size: 0.88rem;
        font-weight: 600;
        margin: 3px;
    }
    .tag-missing {
        display: inline-block;
        background-color: #fee2e2;
        color: #991b1b;
        border: 1px solid #fecaca;
        padding: 4px 10px;
        border-radius: 16px;
        font-size: 0.88rem;
        font-weight: 600;
        margin: 3px;
    }
    .tag-keyword {
        display: inline-block;
        background-color: #e0f2fe;
        color: #075985;
        border: 1px solid #bae6fd;
        padding: 4px 10px;
        border-radius: 16px;
        font-size: 0.88rem;
        font-weight: 500;
        margin: 3px;
    }

    /* Footer / privacy callout */
    .privacy-badge {
        background-color: #f1f5f9;
        border-left: 4px solid #3b82f6;
        padding: 0.75rem 1rem;
        border-radius: 4px;
        font-size: 0.85rem;
        color: #475569;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # ---------------------------------------------------------
    # SIDEBAR
    # ---------------------------------------------------------
    with st.sidebar:
        st.title("🎯 AI Resume Analyzer")
        st.caption("Intelligent Local Resume & JD Matcher")
        st.markdown("---")
        
        st.markdown("### 📋 How It Works")
        st.markdown("""
        1. **Upload Resume**: Provide your resume in **PDF** format.
        2. **Paste Job Description**: Copy & paste the target job description.
        3. **Analyze**: Click the analyze button to get detailed match scores & suggestions.
        """)

        st.markdown("---")
        st.markdown("### 🔒 Privacy First")
        st.info("Your resume is processed entirely **locally in-memory**. No data is stored or uploaded to external APIs.")

        st.markdown("---")
        st.caption("Supported Format: **PDF (.pdf)**")

    # ---------------------------------------------------------
    # MAIN HEADER
    # ---------------------------------------------------------
    st.markdown("""
    <div class="header-banner">
        <h1>AI Resume Analyzer</h1>
        <p>Compare your resume against job descriptions with transparent scoring, skill gap analysis, and actionable insights.</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize Session State
    if "resume_text" not in st.session_state:
        st.session_state.resume_text = None
    if "pdf_metadata" not in st.session_state:
        st.session_state.pdf_metadata = None
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None

    col_left, col_right = st.columns([1, 1], gap="medium")

    # ---------------------------------------------------------
    # STEP 1: RESUME UPLOAD (LEFT COLUMN)
    # ---------------------------------------------------------
    with col_left:
        st.subheader("1. Upload Resume (PDF)")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=["pdf"],
            help="Upload your text-selectable resume in PDF format."
        )

        if uploaded_file is not None:
            try:
                resume_text, metadata = resume_parser.extract_text_from_pdf(uploaded_file)
                st.session_state.resume_text = resume_text
                st.session_state.pdf_metadata = metadata

                st.success(f"Successfully loaded `{metadata['filename']}`!")

                # Display PDF Metadata metrics
                m_col1, m_col2, m_col3 = st.columns(3)
                with m_col1:
                    st.metric("Pages", metadata["num_pages"])
                with m_col2:
                    st.metric("Word Count", metadata["word_count"])
                with m_col3:
                    st.metric("Character Count", metadata["char_count"])

            except resume_parser.ResumeParseException as e:
                st.error(f"❌ {str(e)}")
                st.session_state.resume_text = None
                st.session_state.pdf_metadata = None
            except Exception as e:
                st.error(f"❌ Unexpected error reading PDF: {str(e)}")
                st.session_state.resume_text = None
                st.session_state.pdf_metadata = None

    # ---------------------------------------------------------
    # STEP 2: JOB DESCRIPTION (RIGHT COLUMN)
    # ---------------------------------------------------------
    with col_right:
        st.subheader("2. Paste Job Description")
        jd_input = st.text_area(
            "Job Description Text",
            height=215,
            placeholder="Paste the full job requirements, responsibilities, and qualifications here...",
            help="Include technical requirements, experience, and qualifications."
        )

    # ---------------------------------------------------------
    # STEP 3: ANALYZE BUTTON
    # ---------------------------------------------------------
    st.markdown("---")
    btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
    with btn_col2:
        analyze_clicked = st.button("🚀 Analyze Resume Against Job Description", type="primary", use_container_width=True)

    if analyze_clicked:
        # Validation checks
        if not st.session_state.resume_text:
            st.warning("⚠️ Please upload a valid PDF resume before analyzing.")
        elif not jd_input or len(jd_input.strip()) < 20:
            st.warning("⚠️ Please enter a complete Job Description (at least 20 characters).")
        else:
            with st.spinner("Analyzing resume content, extracting skills, and calculating match score..."):
                results = analyzer.analyze_resume_vs_jd(
                    st.session_state.resume_text,
                    jd_input
                )
                st.session_state.analysis_results = results
                st.success("Analysis complete!")

    # ---------------------------------------------------------
    # RESULTS DASHBOARD
    # ---------------------------------------------------------
    if st.session_state.analysis_results is not None:
        results = st.session_state.analysis_results
        metadata = st.session_state.pdf_metadata
        score = results["match_score"]

        st.markdown("## 📊 Analysis Dashboard")

        # Top Hero Score Box
        st.markdown(f"""
        <div class="score-container">
            <h3 style="margin-bottom: 0.2rem; color: #475569;">RESUME MATCH SCORE</h3>
            <div style="font-size: 3.8rem; font-weight: 800; color: {'#16a34a' if score >= 75 else '#d97706' if score >= 50 else '#dc2626'};">
                {score}%
            </div>
            <p style="color: #64748b; font-size: 0.95rem; margin-top: 0.5rem;">
                Automated match estimate based on transparent weighted criteria (Technical Skills, Keywords, Experience, Education & Similarity).
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(score / 100.0)

        # 4 Key Summary Stat Cards
        stat1, stat2, stat3, stat4 = st.columns(4)
        with stat1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="value" style="color: #16a34a;">{len(results['matched_skills'])}</div>
                <div class="label">Matching Skills</div>
            </div>
            """, unsafe_allow_html=True)
        with stat2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="value" style="color: #dc2626;">{len(results['missing_skills'])}</div>
                <div class="label">Missing Skills</div>
            </div>
            """, unsafe_allow_html=True)
        with stat3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="value" style="color: #0284c7;">{len(results['matched_keywords'])}</div>
                <div class="label">Keywords Matched</div>
            </div>
            """, unsafe_allow_html=True)
        with stat4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="value" style="color: #475569;">{metadata['word_count']}</div>
                <div class="label">Resume Words</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ---------------------------------------------------------
        # TABS FOR DETAILED SECTIONS
        # ---------------------------------------------------------
        tab_overview, tab_skills, tab_keywords, tab_structure, tab_report = st.tabs([
            "📈 Score Overview",
            "🛠️ Skills Analysis",
            "🔍 Keyword Insights",
            "📑 Structure & Quality",
            "📥 Action Plan & Report"
        ])

        # TAB 1: SCORE OVERVIEW & REQUIREMENT SUMMARY
        with tab_overview:
            st.subheader("Transparent Score Breakdown")
            st.write("Here is how your total match score of **{}%** was calculated:".format(score))

            breakdown = results["score_breakdown"]
            breakdown_df = pd.DataFrame([
                {
                    "Evaluation Category": "Technical Skills Match",
                    "Weight": f"{breakdown['technical_skills']['weight_pct']}%",
                    "Category Match": f"{breakdown['technical_skills']['score_pct']}%",
                    "Score Contribution": f"{breakdown['technical_skills']['contribution']} pts"
                },
                {
                    "Evaluation Category": "Keyword Relevance",
                    "Weight": f"{breakdown['keywords']['weight_pct']}%",
                    "Category Match": f"{breakdown['keywords']['score_pct']}%",
                    "Score Contribution": f"{breakdown['keywords']['contribution']} pts"
                },
                {
                    "Evaluation Category": "Experience Alignment",
                    "Weight": f"{breakdown['experience']['weight_pct']}%",
                    "Category Match": f"{breakdown['experience']['score_pct']}%",
                    "Score Contribution": f"{breakdown['experience']['contribution']} pts"
                },
                {
                    "Evaluation Category": "Education Alignment",
                    "Weight": f"{breakdown['education']['weight_pct']}%",
                    "Category Match": f"{breakdown['education']['score_pct']}%",
                    "Score Contribution": f"{breakdown['education']['contribution']} pts"
                },
                {
                    "Evaluation Category": "Overall Textual Similarity",
                    "Weight": f"{breakdown['text_similarity']['weight_pct']}%",
                    "Category Match": f"{breakdown['text_similarity']['score_pct']}%",
                    "Score Contribution": f"{breakdown['text_similarity']['contribution']} pts"
                }
            ])
            st.table(breakdown_df)

            st.subheader("Job Requirement Summary")
            jd_info = results["jd_info"]
            col_a, col_b = st.columns(2)
            with col_a:
                st.info(f"**Experience Requirement:** {jd_info['experience_requirement']}")
            with col_b:
                st.info(f"**Education Requirement:** {jd_info['education_requirement']}")

            st.caption("ℹ️ *Disclaimer: This score is an automated statistical estimate intended for resume optimization and self-assessment, not a definitive recruitment decision.*")

        # TAB 2: SKILLS ANALYSIS
        with tab_skills:
            st.subheader("Skills Comparison")
            
            total_jd_skills = len(results['jd_skills'])
            matched_count = len(results['matched_skills'])
            pct = int(round((matched_count / total_jd_skills * 100))) if total_jd_skills > 0 else 100
            
            st.markdown(f"**Skill Match:** `{matched_count} / {total_jd_skills}` skills matched (**{pct}%**)")

            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.markdown("#### ✅ Skills You Have")
                if results['matched_skills']:
                    tags_html = "".join([f'<span class="tag-matched">{s}</span>' for s in results['matched_skills']])
                    st.markdown(tags_html, unsafe_allow_html=True)
                else:
                    st.write("No matching technical skills detected.")

            with col_s2:
                st.markdown("#### ❌ Skills You May Be Missing")
                if results['missing_skills']:
                    tags_html = "".join([f'<span class="tag-missing">{s}</span>' for s in results['missing_skills']])
                    st.markdown(tags_html, unsafe_allow_html=True)
                    st.caption("Sorted by frequency of occurrence in the Job Description.")
                else:
                    st.success("Great job! You have matched all skills detected in the job description.")

            st.markdown("---")
            st.subheader("Skills Visual Breakdown by Category")
            
            # Prepare data for matplotlib visualization
            categories = list(skills.SKILL_CATEGORIES.keys())
            matched_by_cat = []
            missing_by_cat = []

            for cat in categories:
                cat_canonical_all = [skills.normalize_skill(s) for s in skills.SKILL_CATEGORIES[cat]]
                m_count = sum(1 for s in results['matched_skills'] if s in cat_canonical_all)
                miss_count = sum(1 for s in results['missing_skills'] if s in cat_canonical_all)
                matched_by_cat.append(m_count)
                missing_by_cat.append(miss_count)

            fig, ax = plt.subplots(figsize=(10, 4.5))
            y = np.arange(len(categories))
            height = 0.35

            rects1 = ax.barh(y - height/2, matched_by_cat, height, label='Matched Skills', color='#16a34a')
            rects2 = ax.barh(y + height/2, missing_by_cat, height, label='Missing Skills', color='#dc2626')

            ax.set_xlabel('Count')
            ax.set_title('Matched vs Missing Skills by Category')
            ax.set_yticks(y)
            ax.set_yticklabels(categories)
            ax.legend(loc='lower right')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.tight_layout()

            st.pyplot(fig)

        # TAB 3: KEYWORD INSIGHTS
        with tab_keywords:
            st.subheader("Job Description Keyword Extraction")
            st.write("Important domain terms and keywords extracted from the Job Description:")

            col_k1, col_k2 = st.columns(2)
            with col_k1:
                st.markdown("#### 🎯 Matched Keywords")
                if results['matched_keywords']:
                    tags_html = "".join([f'<span class="tag-keyword">{kw}</span>' for kw in results['matched_keywords']])
                    st.markdown(tags_html, unsafe_allow_html=True)
                else:
                    st.write("No key terms matched.")

            with col_k2:
                st.markdown("#### 🔍 Missing Keywords")
                if results['missing_keywords']:
                    tags_html = "".join([f'<span class="tag-missing">{kw}</span>' for kw in results['missing_keywords']])
                    st.markdown(tags_html, unsafe_allow_html=True)
                else:
                    st.write("No missing key terms!")

        # TAB 4: STRUCTURE & QUALITY CHECK
        with tab_structure:
            col_q1, col_q2 = st.columns(2)
            with col_q1:
                st.subheader("Resume Section Audit")
                for section, found in results["sections_status"].items():
                    if found:
                        st.markdown(f"✅ **{section}**")
                    else:
                        st.markdown(f"❌ <span style='color: #dc2626;'>**{section}** (Missing)</span>", unsafe_allow_html=True)

            with col_q2:
                st.subheader("Quality Feedback & Suggestions")
                for item in results["quality_checks"]:
                    if item["type"] == "good":
                        st.success(f"**{item['title']}**: {item['description']}")
                    elif item["type"] == "warning":
                        st.warning(f"**{item['title']}**: {item['description']}\n\n*Suggestion:* {item['example']}")
                    else:
                        st.info(f"**{item['title']}**: {item['description']}\n\n*Suggestion:* {item['example']}")

        # TAB 5: ACTION PLAN & REPORT DOWNLOAD
        with tab_report:
            st.subheader("💡 How to Improve Your Match Score")
            for idx, rec in enumerate(results["recommendations"], 1):
                st.markdown(f"{idx}. {rec}")

            st.markdown("---")
            st.subheader("📥 Download Analysis Report")
            st.write("Get a complete text report of this analysis to review offline or share.")

            # Generate report text
            report_text = report_generator.generate_text_report(results, metadata)
            report_filename = f"Resume_Analysis_{metadata['filename'].replace('.pdf', '')}.txt"

            st.download_button(
                label="📄 Download Analysis Report (.txt)",
                data=report_text,
                file_name=report_filename,
                mime="text/plain",
                type="primary"
            )

    # Privacy footer note
    st.markdown("""
    <div class="privacy-badge">
        🔒 <b>Privacy Commitment:</b> Your resume is processed locally in-memory. It is not saved to any database or submitted to external AI services.
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
