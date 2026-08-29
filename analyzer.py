"""
analyzer.py
-----------
Matching algorithm, keyword extraction, transparent scoring system,
Job Description parsing, and recommendation engine for AI Resume Analyzer.
"""

import re
from typing import Any, Dict, List, Set, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import skills
from resume_parser import detect_resume_sections, analyze_resume_quality


# Common English stop words plus document boilerplate words to filter out from keywords
CUSTOM_STOP_WORDS = {
    'and', 'the', 'to', 'of', 'a', 'in', 'for', 'is', 'on', 'that', 'by', 'this',
    'with', 'i', 'you', 'it', 'not', 'or', 'be', 'are', 'from', 'at', 'as', 'your',
    'all', 'have', 'new', 'more', 'an', 'was', 'we', 'will', 'home', 'can', 'us',
    'about', 'if', 'page', 'my', 'has', 'search', 'free', 'but', 'our', 'one',
    'other', 'do', 'no', 'information', 'time', 'they', 'site', 'he', 'up', 'may',
    'what', 'which', 'their', 'news', 'out', 'use', 'any', 'there', 'see', 'only',
    'so', 'his', 'when', 'contact', 'here', 'business', 'who', 'web', 'also',
    'now', 'help', 'get', 'pm', 'view', 'online', 'c', 'e', 'first', 'am', 'been',
    'would', 'how', 'were', 'me', 'services', 'some', 'these', 'click', 'its',
    'like', 'service', 'than', 'find', 'price', 'date', 'back', 'top', 'people',
    'had', 'list', 'name', 'just', 'over', 'state', 'year', 'day', 'into', 'email',
    'two', 'health', 'world', 're', 'next', 'used', 'go', 'work', 'last', 'most',
    'buy', 'data', 'make', 'them', 'should', 'product', 'system', 'post', 'her',
    'city', 'add', 'policy', 'number', 'such', 'please', 'available', 'must',
    'job', 'resume', 'candidate', 'applicant', 'opportunity', 'role', 'responsibilities',
    'description', 'position', 'company', 'team', 'working', 'experience', 'years',
    'required', 'requirements', 'preferred', 'qualifications', 'ability', 'strong'
}


def extract_jd_requirements(jd_text: str) -> Dict[str, Any]:
    """
    Parses Job Description text to identify key requirements:
    - Required technical and soft skills
    - Experience requirement (years)
    - Education requirement
    """
    # 1. Skill extraction
    flat_skills = skills.extract_flat_skills(jd_text)
    categorized_skills = skills.extract_skills(jd_text)
    skill_freqs = skills.count_skill_frequencies(jd_text, flat_skills)

    # Sort skills by frequency in JD
    sorted_skills = sorted(flat_skills, key=lambda s: skill_freqs.get(s, 1), reverse=True)

    # 2. Experience level detection
    exp_patterns = [
        r"(\d+[\+\-]?\s*(?:to|-)?\s*\d*)\s*(?:years?|yrs?)\b",
        r"(\d+)\+\s*(?:years?|yrs?)\s+of\s+experience",
        r"(entry\s*level|junior|mid\s*level|senior|lead|principal)"
    ]
    exp_found = []
    for pat in exp_patterns:
        matches = re.findall(pat, jd_text, re.IGNORECASE)
        for m in matches:
            if isinstance(m, tuple):
                exp_found.append(" ".join(m).strip())
            else:
                exp_found.append(m.strip())

    exp_requirement = ", ".join(list(set(exp_found))) if exp_found else "Not explicitly specified"

    # 3. Degree / Education detection
    edu_keywords = ["bachelor", "master", "phd", "degree", "computer science", "b.s", "m.s", "b.tech", "m.tech", "engineering"]
    found_edu = [kw.title() for kw in edu_keywords if re.search(r"\b" + re.escape(kw) + r"\b", jd_text, re.IGNORECASE)]
    edu_requirement = ", ".join(list(set(found_edu))) if found_edu else "Not explicitly specified"

    return {
        "flat_skills": sorted_skills,
        "categorized_skills": categorized_skills,
        "skill_frequencies": skill_freqs,
        "experience_requirement": exp_requirement,
        "education_requirement": edu_requirement
    }


def extract_important_keywords(text: str, top_n: int = 25) -> List[str]:
    """
    Extracts top N meaningful non-skill keywords from text using TF-IDF scoring.
    """
    if not text or len(text.strip()) == 0:
        return []

    try:
        vectorizer = TfidfVectorizer(
            stop_words='english',
            token_pattern=r'(?u)\b[A-Za-z]{3,}\b',
            max_features=100
        )
        tfidf_matrix = vectorizer.fit_transform([text])
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]

        # Filter out custom stop words & standard skills
        all_skills_lower = {s.lower() for s in skills.get_all_skills_flat()}
        
        valid_keywords = []
        for word, score in zip(feature_names, scores):
            word_lower = word.lower()
            if (word_lower not in CUSTOM_STOP_WORDS and 
                word_lower not in all_skills_lower and 
                len(word) > 2):
                valid_keywords.append((word.capitalize(), score))

        # Sort by TF-IDF score
        valid_keywords.sort(key=lambda x: x[1], reverse=True)
        return [kw[0] for kw in valid_keywords[:top_n]]

    except Exception:
        # Fallback keyword extraction using regex split
        words = re.findall(r'\b[A-Za-z]{4,}\b', text)
        filtered = [
            w.capitalize() for w in words 
            if w.lower() not in CUSTOM_STOP_WORDS and 
            w.lower() not in {s.lower() for s in skills.get_all_skills_flat()}
        ]
        unique_words = list(dict.fromkeys(filtered))
        return unique_words[:top_n]


def compute_textual_similarity(text1: str, text2: str) -> float:
    """
    Calculates TF-IDF Cosine Similarity between two text documents (0.0 to 1.0).
    """
    if not text1.strip() or not text2.strip():
        return 0.0

    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf = vectorizer.fit_transform([text1, text2])
        sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return float(sim)
    except Exception:
        return 0.0


def analyze_resume_vs_jd(resume_text: str, jd_text: str) -> Dict[str, Any]:
    """
    Main analysis function. Compares resume against job description.

    Returns comprehensive analysis results including score, breakdown,
    skills comparison, keywords, structure audit, quality feedback, and recommendations.
    """
    # 1. Parse JD requirements
    jd_info = extract_jd_requirements(jd_text)
    jd_skills = jd_info["flat_skills"]

    # 2. Extract Resume skills
    resume_skills = skills.extract_flat_skills(resume_text)
    resume_categorized = skills.extract_skills(resume_text)

    # 3. Skills Comparison
    matched_skills = [s for s in jd_skills if s in resume_skills]
    missing_skills = [s for s in jd_skills if s not in resume_skills]
    extra_skills = [s for s in resume_skills if s not in jd_skills]

    # Sort missing skills by frequency in JD
    missing_skills_sorted = sorted(
        missing_skills,
        key=lambda s: jd_info["skill_frequencies"].get(s, 1),
        reverse=True
    )

    skill_match_ratio = len(matched_skills) / len(jd_skills) if jd_skills else 1.0

    # 4. Keyword Analysis
    jd_keywords = extract_important_keywords(jd_text, top_n=20)
    matched_keywords = []
    missing_keywords = []

    resume_text_lower = resume_text.lower()
    for kw in jd_keywords:
        if re.search(r"\b" + re.escape(kw.lower()) + r"\b", resume_text_lower):
            matched_keywords.append(kw)
        else:
            missing_keywords.append(kw)

    keyword_match_ratio = len(matched_keywords) / len(jd_keywords) if jd_keywords else 1.0

    # 5. Experience & Education Relevance
    # Experience check
    experience_score = 0.0
    sections = detect_resume_sections(resume_text)
    if sections.get("Experience", False):
        experience_score += 0.6
    
    # Check if years of experience matches if requested in JD
    if jd_info["experience_requirement"] != "Not explicitly specified":
        # Check for numbers/years in resume
        if re.search(r"\b\d+\+?\s*(?:years?|yrs?)\b", resume_text_lower):
            experience_score += 0.4
    else:
        experience_score += 0.4

    experience_score = min(1.0, experience_score)

    # Education check
    education_score = 0.0
    if sections.get("Education", False):
        education_score += 0.6

    if jd_info["education_requirement"] != "Not explicitly specified":
        edu_terms = ["bachelor", "master", "degree", "bs", "ms", "computer science", "engineering"]
        if any(re.search(r"\b" + term + r"\b", resume_text_lower) for term in edu_terms):
            education_score += 0.4
    else:
        education_score += 0.4

    education_score = min(1.0, education_score)

    # 6. Overall Textual Similarity
    text_similarity = compute_textual_similarity(resume_text, jd_text)

    # 7. Transparent Match Score Calculation
    # Default Base Weights:
    # 40% Technical Skills, 20% Keywords, 15% Experience, 15% Education, 10% Text Similarity
    w_skills = 0.40
    w_keywords = 0.20
    w_exp = 0.15
    w_edu = 0.15
    w_text = 0.10

    # Adjust weights if JD has zero technical skills listed
    if not jd_skills:
        w_keywords += 0.25
        w_text += 0.15
        w_skills = 0.0

    weighted_score = (
        (skill_match_ratio * w_skills) +
        (keyword_match_ratio * w_keywords) +
        (experience_score * w_exp) +
        (education_score * w_edu) +
        (text_similarity * w_text)
    )

    overall_match_score = int(round(weighted_score * 100))
    overall_match_score = max(0, min(100, overall_match_score))

    # Score breakdown details for UI transparent display
    score_breakdown = {
        "technical_skills": {
            "weight_pct": int(w_skills * 100),
            "score_pct": int(round(skill_match_ratio * 100)),
            "contribution": round(skill_match_ratio * w_skills * 100, 1)
        },
        "keywords": {
            "weight_pct": int(w_keywords * 100),
            "score_pct": int(round(keyword_match_ratio * 100)),
            "contribution": round(keyword_match_ratio * w_keywords * 100, 1)
        },
        "experience": {
            "weight_pct": int(w_exp * 100),
            "score_pct": int(round(experience_score * 100)),
            "contribution": round(experience_score * w_exp * 100, 1)
        },
        "education": {
            "weight_pct": int(w_edu * 100),
            "score_pct": int(round(education_score * 100)),
            "contribution": round(education_score * w_edu * 100, 1)
        },
        "text_similarity": {
            "weight_pct": int(w_text * 100),
            "score_pct": int(round(text_similarity * 100)),
            "contribution": round(text_similarity * w_text * 100, 1)
        }
    }

    # 8. Resume Quality Analysis
    quality_checks = analyze_resume_quality(resume_text, sections)

    # 9. Generate Personalized Recommendations
    recommendations = generate_recommendations(
        missing_skills=missing_skills_sorted,
        missing_keywords=missing_keywords,
        sections_found=sections,
        quality_checks=quality_checks,
        skill_ratio=skill_match_ratio
    )

    return {
        "match_score": overall_match_score,
        "score_breakdown": score_breakdown,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills_sorted,
        "extra_skills": extra_skills,
        "resume_skills": resume_skills,
        "resume_categorized_skills": resume_categorized,
        "jd_skills": jd_skills,
        "jd_info": jd_info,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "sections_status": sections,
        "quality_checks": quality_checks,
        "recommendations": recommendations,
        "text_similarity_pct": int(round(text_similarity * 100))
    }


def generate_recommendations(
    missing_skills: List[str],
    missing_keywords: List[str],
    sections_found: Dict[str, bool],
    quality_checks: List[Dict[str, str]],
    skill_ratio: float
) -> List[str]:
    """
    Generates honest, actionable advice to help candidate tailor their resume.
    Explicitly instructs user never to fabricate skills.
    """
    recs = []

    # Missing critical skills advice
    if missing_skills:
        top_missing = missing_skills[:5]
        recs.append(
            f"**Add Relevant Key Technologies**: If you have hands-on experience with "
            f"**{', '.join(top_missing)}**, make sure to explicitly include them in your Skills section or project bullet points."
        )

    # Missing sections advice
    missing_sec = [sec for sec, found in sections_found.items() if not found and sec in ["Education", "Experience", "Projects", "Skills"]]
    if missing_sec:
        recs.append(
            f"**Add Essential Resume Sections**: Your resume appears to be missing standard section headers for "
            f"**{', '.join(missing_sec)}**. Adding clear headings helps both ATS parsers and human reviewers."
        )

    # Missing industry keywords advice
    if missing_keywords:
        top_kw = missing_keywords[:4]
        recs.append(
            f"**Incorporate Key Domain Terms**: Consider weaving domain terms like **{', '.join(top_kw)}** "
            f"into your experience narrative where applicable."
        )

    # Quality check suggestions
    for check in quality_checks:
        if check["type"] in ["warning", "tip"] and check["example"]:
            recs.append(f"**{check['title']}**: {check['description']} ({check['example']})")

    # General best practice recommendation
    recs.append(
        "**Quantify Accomplishments**: Frame project bullet points with metrics (e.g. 'Reduced loading latency by 25%' or 'Managed a dataset of 10,000+ records')."
    )

    # Mandatory Integrity Notice
    recs.append(
        "⚠️ **Honesty & Integrity Reminder**: Only add skills, tools, or experiences that you genuinely possess. "
        "Never add false skills solely to boost an automated score."
    )

    return recs
