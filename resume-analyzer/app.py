"""
app.py
------
Main Streamlit application interface for AI Resume Analyzer.
Crafted with a bespoke editorial aesthetic inspired by Swiss design principles,
warm cream tones, serif display headers, and refined pill badges.
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
    page_title="AI Resume Analyzer — Editorial Dashboard",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Artisanal Editorial Custom CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* Global Background & Typography */
    .stApp {
        background-color: #f7f5f0;
        color: #1a1918;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }

    /* Main container layout */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1140px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #efece4 !important;
        border-right: 1px solid #e0dad0;
    }
    section[data-testid="stSidebar"] .stMarkdown h1, 
    section[data-testid="stSidebar"] .stMarkdown h2, 
    section[data-testid="stSidebar"] .stMarkdown h3 {
        font-family: 'Instrument Serif', Georgia, serif;
        color: #1a1918;
        font-weight: 500;
        letter-spacing: -0.01em;
    }

    /* Custom Editorial Header Banner */
    .editorial-header {
        background-color: #f0ece1;
        border: 1px solid #dbd4c5;
        border-radius: 16px;
        padding: 2.5rem 2.5rem 2.2rem 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }
    .editorial-header h1 {
        font-family: 'Instrument Serif', Georgia, serif;
        font-size: 3.2rem;
        font-weight: 400;
        color: #1a1918;
        margin-bottom: 0.4rem;
        line-height: 1.1;
        letter-spacing: -0.02em;
    }
    .editorial-header p {
        font-size: 1.1rem;
        color: #57524a;
        margin-bottom: 0;
        font-weight: 400;
        line-height: 1.5;
    }

    /* Cards & Containers */
    .editorial-card {
        background-color: #ffffff;
        border: 1px solid #e6e0d4;
        border-radius: 14px;
        padding: 1.5rem;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02);
        margin-bottom: 1rem;
    }
    .metric-value {
        font-family: 'Instrument Serif', Georgia, serif;
        font-size: 2.8rem;
        font-weight: 400;
        color: #1a1918;
        line-height: 1;
    }
    .metric-label {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #787166;
        margin-top: 0.4rem;
    }

    /* Hero Score Box */
    .hero-score-box {
        background-color: #ffffff;
        border: 1px solid #ded7c8;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
    }
    .hero-score-number {
        font-family: 'Instrument Serif', Georgia, serif;
        font-size: 5rem;
        font-weight: 400;
        line-height: 1;
        margin: 0.5rem 0;
    }
    .hero-score-label {
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #787166;
    }

    /* Bespoke Pill Badges */
    .pill-matched {
        display: inline-block;
        background-color: #e2ede2;
        color: #1b431b;
        border: 1px solid #c5dcc5;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.86rem;
        font-weight: 600;
        margin: 4px;
    }
    .pill-missing {
        display: inline-block;
        background-color: #f7e8d7;
        color: #6e3f10;
        border: 1px solid #ead0b3;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.86rem;
        font-weight: 600;
        margin: 4px;
    }
    .pill-keyword {
        display: inline-block;
        background-color: #e5edf5;
        color: #1c3b57;
        border: 1px solid #cadbe8;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.86rem;
        font-weight: 500;
        margin: 4px;
    }

    /* Headings in Main Body */
    h1, h2, h3 {
        font-family: 'Instrument Serif', Georgia, serif !important;
        color: #1a1918 !important;
        font-weight: 500 !important;
    }

    /* Progress bar custom color styling */
    div[data-baseweb="progress-bar"] > div {
        background-color: #dcd6c8 !important;
    }
    div[data-baseweb="progress-bar"] div[role="progressbar"] {
        background-color: #2d4a34 !important;
    }

    /* Privacy Banner */
    .privacy-box {
        background-color: #efece4;
        border: 1px solid #dbd4c5;
        border-left: 4px solid #2d4a34;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        font-size: 0.88rem;
        color: #47433c;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # ---------------------------------------------------------
    # SIDEBAR
    # ---------------------------------------------------------
    with st.sidebar:
        st.markdown("# AI Resume Analyzer")
        st.markdown("*Boutique Candidate Evaluation Engine*")
        st.markdown("---")
        
        st.markdown("### Workflow")
        st.markdown("""
        1. **Upload Resume**: Provide a readable PDF resume.
        2. **Paste Job Description**: Copy & paste target job text.
        3. **Analyze**: Inspect bespoke compatibility metrics.
        """)

        st.markdown("---")
        st.markdown("### Privacy Commitment")
        st.info("Your data is processed strictly **in-memory locally**. No resumes are stored or sent to third-party AI APIs.")

        st.markdown("---")
        st.caption("Engine Version 1.0 • Swiss Minimalist Edition")

    # ---------------------------------------------------------
    # MAIN HEADER
    # ---------------------------------------------------------
    st.markdown("""
    <div class="editorial-header">
        <h1>AI Resume Analyzer</h1>
        <p>Evaluate resume alignment against target job descriptions with transparent scoring, structured skill mapping, and editorial quality auditing.</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize Session State
    if "resume_text" not in st.session_state:
        st.session_state.resume_text = None
    if "pdf_metadata" not in st.session_state:
        st.session_state.pdf_metadata = None
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None

    col_left, col_right = st.columns([1, 1], gap="large")

    # ---------------------------------------------------------
    # STEP 1: RESUME UPLOAD (LEFT COLUMN)
    # ---------------------------------------------------------
    with col_left:
        st.markdown("## 1. Resume Document")
        uploaded_file = st.file_uploader(
            "Upload PDF Resume",
            type=["pdf"],
            help="Select a text-selectable PDF document."
        )

        if uploaded_file is not None:
            try:
                resume_text, metadata = resume_parser.extract_text_from_pdf(uploaded_file)
                st.session_state.resume_text = resume_text
                st.session_state.pdf_metadata = metadata

                st.success(f"Loaded `{metadata['filename']}`")

                # Display PDF Metadata metrics in clean editorial cards
                m_col1, m_col2, m_col3 = st.columns(3)
                with m_col1:
                    st.markdown(f"""
                    <div class="editorial-card" style="text-align: center; padding: 1rem;">
                        <div class="metric-value">{metadata['num_pages']}</div>
                        <div class="metric-label">Pages</div>
                    </div>
                    """, unsafe_allow_html=True)
                with m_col2:
                    st.markdown(f"""
                    <div class="editorial-card" style="text-align: center; padding: 1rem;">
                        <div class="metric-value">{metadata['word_count']}</div>
                        <div class="metric-label">Words</div>
                    </div>
                    """, unsafe_allow_html=True)
                with m_col3:
                    st.markdown(f"""
                    <div class="editorial-card" style="text-align: center; padding: 1rem;">
                        <div class="metric-value">{metadata['char_count']}</div>
                        <div class="metric-label">Characters</div>
                    </div>
                    """, unsafe_allow_html=True)

            except resume_parser.ResumeParseException as e:
                st.error(f"❌ {str(e)}")
                st.session_state.resume_text = None
                st.session_state.pdf_metadata = None
            except Exception as e:
                st.error(f"❌ Error reading PDF: {str(e)}")
                st.session_state.resume_text = None
                st.session_state.pdf_metadata = None

    # ---------------------------------------------------------
    # STEP 2: JOB DESCRIPTION (RIGHT COLUMN)
    # ---------------------------------------------------------
    with col_right:
        st.markdown("## 2. Job Specification")
        jd_input = st.text_area(
            "Target Job Description",
            height=215,
            placeholder="Paste the full job requirements, key responsibilities, and qualifications here...",
            help="Paste text from job posting."
        )

    # ---------------------------------------------------------
    # STEP 3: ANALYZE BUTTON
    # ---------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
    with btn_col2:
        analyze_clicked = st.button("Analyze Compatibility Report", type="primary", use_container_width=True)

    if analyze_clicked:
        if not st.session_state.resume_text:
            st.warning("Please upload a valid PDF resume before starting analysis.")
        elif not jd_input or len(jd_input.strip()) < 20:
            st.warning("Please enter a complete Job Description (at least 20 characters).")
        else:
            with st.spinner("Processing document text & matching skills..."):
                results = analyzer.analyze_resume_vs_jd(
                    st.session_state.resume_text,
                    jd_input
                )
                st.session_state.analysis_results = results
                st.success("Analysis complete.")

    # ---------------------------------------------------------
    # RESULTS DASHBOARD
    # ---------------------------------------------------------
    if st.session_state.analysis_results is not None:
        results = st.session_state.analysis_results
        metadata = st.session_state.pdf_metadata
        score = results["match_score"]

        st.markdown("<hr style='border-top: 1px solid #dbd4c5; margin: 2.5rem 0;'>", unsafe_allow_html=True)
        st.markdown("## Analysis Dashboard")

        # Color token selection based on score range
        score_color = "#2d4a34" if score >= 75 else "#703c15" if score >= 50 else "#8b2626"

        # Hero Score Box
        st.markdown(f"""
        <div class="hero-score-box">
            <div class="hero-score-label">Resume Match Index</div>
            <div class="hero-score-number" style="color: {score_color};">{score}%</div>
            <p style="color: #696257; font-size: 0.95rem; margin-bottom: 0;">
                Calculated via weighted metrics across Technical Skills, Keyword Relevance, Experience, Education, and Text Similarity.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(score / 100.0)

        # 4 Editorial Stat Cards
        stat1, stat2, stat3, stat4 = st.columns(4)
        with stat1:
            st.markdown(f"""
            <div class="editorial-card" style="text-align: center;">
                <div class="metric-value" style="color: #2d4a34;">{len(results['matched_skills'])}</div>
                <div class="metric-label">Matching Skills</div>
            </div>
            """, unsafe_allow_html=True)
        with stat2:
            st.markdown(f"""
            <div class="editorial-card" style="text-align: center;">
                <div class="metric-value" style="color: #8b2626;">{len(results['missing_skills'])}</div>
                <div class="metric-label">Missing Skills</div>
            </div>
            """, unsafe_allow_html=True)
        with stat3:
            st.markdown(f"""
            <div class="editorial-card" style="text-align: center;">
                <div class="metric-value" style="color: #1c3b57;">{len(results['matched_keywords'])}</div>
                <div class="metric-label">Keywords Matched</div>
            </div>
            """, unsafe_allow_html=True)
        with stat4:
            st.markdown(f"""
            <div class="editorial-card" style="text-align: center;">
                <div class="metric-value" style="color: #47433c;">{metadata['word_count']}</div>
                <div class="metric-label">Total Words</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ---------------------------------------------------------
        # TABS FOR DETAILED SECTIONS
        # ---------------------------------------------------------
        tab_overview, tab_skills, tab_keywords, tab_structure, tab_report = st.tabs([
            "Score Breakdown",
            "Skill Mapping",
            "Keyword Insights",
            "Structure & Quality",
            "Action Plan & Download"
        ])

        # TAB 1: SCORE OVERVIEW & REQUIREMENT SUMMARY
        with tab_overview:
            st.markdown("### Transparent Score Allocation")
            st.write(f"The overall match index of **{score}%** comprises the following evaluated components:")

            breakdown = results["score_breakdown"]
            breakdown_df = pd.DataFrame([
                {
                    "Evaluation Domain": "Technical Skills Match",
                    "Weight": f"{breakdown['technical_skills']['weight_pct']}%",
                    "Domain Score": f"{breakdown['technical_skills']['score_pct']}%",
                    "Points Contributed": f"{breakdown['technical_skills']['contribution']} pts"
                },
                {
                    "Evaluation Domain": "Keyword Relevance",
                    "Weight": f"{breakdown['keywords']['weight_pct']}%",
                    "Domain Score": f"{breakdown['keywords']['score_pct']}%",
                    "Points Contributed": f"{breakdown['keywords']['contribution']} pts"
                },
                {
                    "Evaluation Domain": "Experience Alignment",
                    "Weight": f"{breakdown['experience']['weight_pct']}%",
                    "Domain Score": f"{breakdown['experience']['score_pct']}%",
                    "Points Contributed": f"{breakdown['experience']['contribution']} pts"
                },
                {
                    "Evaluation Domain": "Education Alignment",
                    "Weight": f"{breakdown['education']['weight_pct']}%",
                    "Domain Score": f"{breakdown['education']['score_pct']}%",
                    "Points Contributed": f"{breakdown['education']['contribution']} pts"
                },
                {
                    "Evaluation Domain": "Textual Similarity",
                    "Weight": f"{breakdown['text_similarity']['weight_pct']}%",
                    "Domain Score": f"{breakdown['text_similarity']['score_pct']}%",
                    "Points Contributed": f"{breakdown['text_similarity']['contribution']} pts"
                }
            ])
            st.table(breakdown_df)

            st.markdown("### Job Specification Overview")
            jd_info = results["jd_info"]
            col_a, col_b = st.columns(2)
            with col_a:
                st.info(f"**Experience Requirement:** {jd_info['experience_requirement']}")
            with col_b:
                st.info(f"**Education Requirement:** {jd_info['education_requirement']}")

            st.caption("Notice: This index is an automated diagnostic estimate designed to assist resume optimization.")

        # TAB 2: SKILLS ANALYSIS
        with tab_skills:
            st.markdown("### Technical Skill Matrix")
            
            total_jd_skills = len(results['jd_skills'])
            matched_count = len(results['matched_skills'])
            pct = int(round((matched_count / total_jd_skills * 100))) if total_jd_skills > 0 else 100
            
            st.markdown(f"**Overall Skill Match:** `{matched_count} of {total_jd_skills}` skills identified (**{pct}%**)")

            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.markdown("#### Matched Skills")
                if results['matched_skills']:
                    pills_html = "".join([f'<span class="pill-matched">{s}</span>' for s in results['matched_skills']])
                    st.markdown(pills_html, unsafe_allow_html=True)
                else:
                    st.write("No matching technical skills detected.")

            with col_s2:
                st.markdown("#### Missing Skills")
                if results['missing_skills']:
                    pills_html = "".join([f'<span class="pill-missing">{s}</span>' for s in results['missing_skills']])
                    st.markdown(pills_html, unsafe_allow_html=True)
                    st.caption("Ordered by frequency in job description.")
                else:
                    st.success("All required job skills were detected on your resume.")

            st.markdown("<hr style='border-top: 1px solid #e0dad0; margin: 2rem 0;'>", unsafe_allow_html=True)
            st.markdown("### Skill Distribution by Category")
            
            # Matplotlib visual styled with cream background and sage/terracotta palette
            categories = list(skills.SKILL_CATEGORIES.keys())
            matched_by_cat = []
            missing_by_cat = []

            for cat in categories:
                cat_canonical_all = [skills.normalize_skill(s) for s in skills.SKILL_CATEGORIES[cat]]
                m_count = sum(1 for s in results['matched_skills'] if s in cat_canonical_all)
                miss_count = sum(1 for s in results['missing_skills'] if s in cat_canonical_all)
                matched_by_cat.append(m_count)
                missing_by_cat.append(miss_count)

            fig, ax = plt.subplots(figsize=(10, 4.2))
            fig.patch.set_facecolor('#f7f5f0')
            ax.set_facecolor('#f7f5f0')

            y = np.arange(len(categories))
            height = 0.35

            rects1 = ax.barh(y - height/2, matched_by_cat, height, label='Matched Skills', color='#2d4a34')
            rects2 = ax.barh(y + height/2, missing_by_cat, height, label='Missing Skills', color='#a8523b')

            ax.set_xlabel('Skill Count', fontsize=10, color='#1a1918')
            ax.set_title('Skill Alignment Breakdown Across Categories', fontsize=12, pad=12, color='#1a1918', fontfamily='Georgia')
            ax.set_yticks(y)
            ax.set_yticklabels(categories, fontsize=9, color='#1a1918')
            ax.legend(loc='lower right', frameon=True, facecolor='#ffffff', edgecolor='#dbd4c5')
            
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#dbd4c5')
            ax.spines['bottom'].set_color('#dbd4c5')
            ax.tick_params(colors='#1a1918')
            plt.tight_layout()

            st.pyplot(fig)

        # TAB 3: KEYWORD INSIGHTS
        with tab_keywords:
            st.markdown("### Domain Terminology & Keywords")
            st.write("Significant non-skill industry terms extracted via TF-IDF text analysis:")

            col_k1, col_k2 = st.columns(2)
            with col_k1:
                st.markdown("#### Matched Keywords")
                if results['matched_keywords']:
                    pills_html = "".join([f'<span class="pill-keyword">{kw}</span>' for kw in results['matched_keywords']])
                    st.markdown(pills_html, unsafe_allow_html=True)
                else:
                    st.write("No direct key term matches found.")

            with col_k2:
                st.markdown("#### Missing Keywords")
                if results['missing_keywords']:
                    pills_html = "".join([f'<span class="pill-missing">{kw}</span>' for kw in results['missing_keywords']])
                    st.markdown(pills_html, unsafe_allow_html=True)
                else:
                    st.write("No missing key terms identified.")

        # TAB 4: STRUCTURE & QUALITY CHECK
        with tab_structure:
            col_q1, col_q2 = st.columns(2)
            with col_q1:
                st.markdown("### Section Audit")
                for section, found in results["sections_status"].items():
                    if found:
                        st.markdown(f"✓ **{section}**")
                    else:
                        st.markdown(f"✗ <span style='color: #8b2626;'>**{section}** (Missing)</span>", unsafe_allow_html=True)

            with col_q2:
                st.markdown("### Editorial Quality Audit")
                for item in results["quality_checks"]:
                    if item["type"] == "good":
                        st.success(f"**{item['title']}**: {item['description']}")
                    elif item["type"] == "warning":
                        st.warning(f"**{item['title']}**: {item['description']}\n\n*Suggestion:* {item['example']}")
                    else:
                        st.info(f"**{item['title']}**: {item['description']}\n\n*Suggestion:* {item['example']}")

        # TAB 5: ACTION PLAN & REPORT DOWNLOAD
        with tab_report:
            st.markdown("### Recommended Optimization Steps")
            for idx, rec in enumerate(results["recommendations"], 1):
                st.markdown(f"{idx}. {rec}")

            st.markdown("<hr style='border-top: 1px solid #e0dad0; margin: 2rem 0;'>", unsafe_allow_html=True)
            st.markdown("### Export Analysis Report")
            st.write("Generate a comprehensive plain-text publication summary for your records:")

            report_text = report_generator.generate_text_report(results, metadata)
            report_filename = f"Resume_Analysis_{metadata['filename'].replace('.pdf', '')}.txt"

            st.download_button(
                label="Download Full Analysis Report (.txt)",
                data=report_text,
                file_name=report_filename,
                mime="text/plain",
                type="primary"
            )

    # Privacy footer callout
    st.markdown("""
    <div class="privacy-box">
        🔒 <b>Local Processing Guarantee:</b> All document parsing and text analysis are executed locally in memory. No resume data is stored on disk or shared with cloud AI services.
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
