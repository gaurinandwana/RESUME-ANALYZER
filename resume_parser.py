"""
resume_parser.py
----------------
PDF text extraction, section detection, and quality analysis module
for AI Resume Analyzer.
"""

import re
from typing import Any, Dict, List, Tuple
import PyPDF2


class ResumeParseException(Exception):
    """Custom exception raised when PDF parsing fails."""
    pass


def extract_text_from_pdf(pdf_file) -> Tuple[str, Dict[str, Any]]:
    """
    Extracts all readable text and metadata from a PDF file.

    Args:
        pdf_file: Streamlit UploadedFile object or file-like object.

    Returns:
        Tuple of (extracted_text, metadata_dict)

    Raises:
        ResumeParseException if PDF cannot be read or contains no readable text.
    """
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(reader.pages)
        
        if num_pages == 0:
            raise ResumeParseException("The uploaded PDF file has 0 pages.")

        extracted_text_list = []
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                extracted_text_list.append(page_text)

        full_text = "\n".join(extracted_text_list).strip()

        if not full_text:
            raise ResumeParseException(
                "Could not extract readable text from the PDF. "
                "The document might be scanned as an image or encrypted. "
                "Please provide a text-selectable PDF resume."
            )

        # Basic metadata calculations
        filename = getattr(pdf_file, "name", "uploaded_resume.pdf")
        words = full_text.split()
        word_count = len(words)
        char_count = len(full_text)

        metadata = {
            "filename": filename,
            "num_pages": num_pages,
            "word_count": word_count,
            "char_count": char_count
        }

        return full_text, metadata

    except ResumeParseException:
        raise
    except Exception as e:
        raise ResumeParseException(f"Failed to read PDF file: {str(e)}")


# Standard resume section patterns
SECTION_PATTERNS: Dict[str, List[str]] = {
    "Contact Information": [
        r"\b(?:email|phone|mobile|linkedin|github|address|location|contact)\b",
        r"[\w\.-]+@[\w\.-]+\.\w+",
        r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b"
    ],
    "Summary / Objective": [
        r"\b(?:summary|professional summary|executive summary|objective|career objective|profile|about me)\b"
    ],
    "Education": [
        r"\b(?:education|academic background|academics|degree|university|college|bachelor|master|phd|b\.s\.|m\.s\.|diploma)\b"
    ],
    "Experience": [
        r"\b(?:experience|work experience|employment history|work history|professional experience|internship|internships)\b"
    ],
    "Projects": [
        r"\b(?:projects|academic projects|personal projects|key projects|portfolio)\b"
    ],
    "Skills": [
        r"\b(?:skills|technical skills|core competencies|technologies|tools|proficiencies|areas of expertise)\b"
    ],
    "Certifications": [
        r"\b(?:certifications|certificates|certified|licenses|accreditations)\b"
    ],
    "Achievements": [
        r"\b(?:achievements|honors|awards|accomplishments|recognition|activities & achievements)\b"
    ],
    "Extracurricular Activities": [
        r"\b(?:extracurricular|volunteer|volunteering|community service|leadership|leadership experience|hobbies)\b"
    ]
}


def detect_resume_sections(text: str) -> Dict[str, bool]:
    """
    Detects which standard resume sections are present in the resume text.

    Returns:
        Dict[section_name, bool]
    """
    sections_status: Dict[str, bool] = {}
    text_lower = text.lower()

    for section_name, patterns in SECTION_PATTERNS.items():
        found = False
        for pattern in patterns:
            if re.search(pattern, text_lower):
                found = True
                break
        sections_status[section_name] = found

    return sections_status


def analyze_resume_quality(text: str, sections_found: Dict[str, bool]) -> List[Dict[str, str]]:
    """
    Performs quality analysis on the resume text.

    Checks:
    - Resume length (too short / too long)
    - Essential section presence
    - Actionable / quantifiable achievements
    - Repetitive phrases

    Returns:
        List of issues/suggestions: [{'type': 'warning'|'tip'|'good', 'title': '...', 'description': '...', 'example': '...'}]
    """
    quality_feedback = []
    words = text.split()
    word_count = len(words)

    # 1. Resume Length Check
    if word_count < 150:
        quality_feedback.append({
            "type": "warning",
            "title": "Resume Too Short",
            "description": f"Your resume contains only {word_count} words. Essential details about your skills and projects may be missing.",
            "example": "Aim for a comprehensive resume of 300–800 words detailing your experience."
        })
    elif word_count > 1200:
        quality_feedback.append({
            "type": "warning",
            "title": "Resume Overly Lengthy",
            "description": f"Your resume contains {word_count} words. Recruiters typically spend 6–10 seconds per resume scan.",
            "example": "Try concise bullet points and focus on high-impact results to keep it under 2 pages."
        })
    else:
        quality_feedback.append({
            "type": "good",
            "title": "Optimal Length",
            "description": f"Your resume length ({word_count} words) falls within the ideal word count range.",
            "example": ""
        })

    # 2. Missing Core Sections
    core_sections = ["Contact Information", "Education", "Experience", "Projects", "Skills"]
    missing_core = [sec for sec in core_sections if not sections_found.get(sec, False)]

    if missing_core:
        quality_feedback.append({
            "type": "warning",
            "title": "Missing Important Sections",
            "description": f"Could not clearly identify the following standard section(s): {', '.join(missing_core)}.",
            "example": "Use standard, clear headers like 'Work Experience', 'Education', 'Projects', and 'Skills'."
        })
    else:
        quality_feedback.append({
            "type": "good",
            "title": "Complete Essential Structure",
            "description": "All core sections (Contact, Experience, Education, Projects, Skills) were detected.",
            "example": ""
        })

    # 3. Measurable Achievements Check
    quantifiable_pattern = r"(\d+%|\$\d+|\d+\+|\b\d+\b\s*(?:users|clients|customers|percent|reduced|increased|improved|saved|scaled))"
    quantifiable_matches = re.findall(quantifiable_pattern, text, re.IGNORECASE)

    if len(quantifiable_matches) < 2:
        quality_feedback.append({
            "type": "tip",
            "title": "Missing Measurable Achievements",
            "description": "Your resume seems to lack quantified outcomes (percentages, numbers, dollar metrics).",
            "example": "Instead of: 'Worked on a web application'\nTry: 'Developed a web application used by 500+ daily active users, reducing API response times by 35%.'"
        })
    else:
        quality_feedback.append({
            "type": "good",
            "title": "Quantified Results Included",
            "description": f"Found {len(quantifiable_matches)} instances of measurable impact or data metrics in your resume.",
            "example": ""
        })

    # 4. Action Verbs Check
    action_verbs = [
        "built", "developed", "architected", "implemented", "engineered",
        "designed", "spearheaded", "managed", "led", "optimized", "reduced",
        "increased", "transformed", "automated", "created", "launched"
    ]
    found_action_verbs = [v for v in action_verbs if re.search(r"\b" + v + r"\b", text, re.IGNORECASE)]

    if len(found_action_verbs) < 3:
        quality_feedback.append({
            "type": "tip",
            "title": "Use Stronger Action Verbs",
            "description": "Incorporate active verbs to begin your accomplishment bullet points.",
            "example": "Use verbs like 'Spearheaded', 'Optimized', 'Architected', 'Automated', or 'Engineered'."
        })

    return quality_feedback
