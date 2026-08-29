"""
skills.py
---------
Skill database and skill extraction module for AI Resume Analyzer.
Contains predefined lists of technical and soft skills, regex patterns,
and normalization utilities.
"""

import re
from typing import Dict, List, Set, Tuple

# Predefined Skill Database categorized for structured analysis
SKILL_CATEGORIES: Dict[str, List[str]] = {
    "Programming Languages": [
        "Python", "Java", "C++", "C", "C#", "JavaScript", "TypeScript",
        "HTML", "CSS", "SQL", "R", "Go", "Golang", "Rust", "PHP",
        "Ruby", "Swift", "Kotlin", "MATLAB", "Bash", "Shell", "PowerShell"
    ],
    "Frameworks & Libraries": [
        "React", "React.js", "ReactJS", "Node.js", "NodeJS", "Express", "Express.js",
        "Django", "Flask", "FastAPI", "Spring", "Spring Boot", "Angular", "Vue.js",
        "Next.js", "Bootstrap", "Tailwind", "Tailwind CSS", "jQuery", "Redux"
    ],
    "Databases": [
        "MySQL", "PostgreSQL", "MongoDB", "Oracle", "Redis", "SQLite",
        "DynamoDB", "Cassandra", "MariaDB", "Firebase", "Supabase"
    ],
    "Cloud & DevOps": [
        "AWS", "Amazon Web Services", "Azure", "GCP", "Google Cloud",
        "Docker", "Kubernetes", "Git", "GitHub", "GitLab", "CI/CD",
        "Terraform", "Ansible", "Linux", "NGINX", "Jenkins"
    ],
    "AI / ML & Data Science": [
        "Machine Learning", "Deep Learning", "Artificial Intelligence", "AI",
        "NLP", "Natural Language Processing", "Data Science", "Data Analysis",
        "TensorFlow", "PyTorch", "Scikit-learn", "sklearn", "Pandas", "NumPy",
        "OpenCV", "LangChain", "Hugging Face", "Keras", "Matplotlib", "Seaborn"
    ],
    "Developer Tools & Web": [
        "REST API", "RESTful API", "GraphQL", "Microservices", "Agile", "Scrum",
        "JIRA", "Unit Testing", "System Design", "OOP", "Object-Oriented Programming"
    ],
    "Soft Skills": [
        "Communication", "Leadership", "Problem Solving", "Teamwork",
        "Time Management", "Critical Thinking", "Adaptability", "Collaboration",
        "Project Management", "Analytical Skills", "Creativity", "Work Ethic"
    ]
}

# Mapping skill variants to a canonical display name
SKILL_CANONICAL_MAP: Dict[str, str] = {
    "react.js": "React",
    "reactjs": "React",
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "express.js": "Express",
    "golang": "Go",
    "amazon web services": "AWS",
    "google cloud": "GCP",
    "google cloud platform": "GCP",
    "sklearn": "Scikit-learn",
    "natural language processing": "NLP",
    "artificial intelligence": "Artificial Intelligence",
    "restful api": "REST API",
    "rest apis": "REST API",
    "object-oriented programming": "OOP",
    "tailwind css": "Tailwind",
}


def normalize_skill(skill: str) -> str:
    """Returns canonical display name for a given skill string."""
    skill_clean = skill.strip()
    skill_lower = skill_clean.lower()
    return SKILL_CANONICAL_MAP.get(skill_lower, skill_clean)


def get_all_skills_flat() -> List[str]:
    """Returns a flat list of all predefined unique skills (canonical names)."""
    unique_skills: Set[str] = set()
    for cat, skill_list in SKILL_CATEGORIES.items():
        for s in skill_list:
            unique_skills.add(normalize_skill(s))
    return sorted(list(unique_skills))


def _build_skill_regex(skill: str) -> re.Pattern:
    """
    Constructs a robust regular expression pattern for matching a skill.
    Handles special characters like C++, C#, .NET, Node.js, etc.
    """
    escaped = re.escape(skill)
    # Special handling for single letter / trailing special char skills like C, C++, C#
    if skill == "C":
        pattern = r"(?<![A-Za-z0-9+#])C(?![A-Za-z0-9+#])"
    elif skill in ["C++", "C#"]:
        pattern = r"(?<![A-Za-z0-9])" + re.escape(skill) + r"(?![A-Za-z0-9])"
    elif skill in ["R"]:
        pattern = r"(?<![A-Za-z0-9])R(?![A-Za-z0-9])"
    elif skill == "AI":
        pattern = r"(?<![A-Za-z0-9])AI(?![A-Za-z0-9])"
    else:
        # standard word boundary matching
        pattern = r"\b" + escaped + r"\b"
    
    return re.compile(pattern, re.IGNORECASE)


def extract_skills(text: str) -> Dict[str, List[str]]:
    """
    Extracts all skills found in the given text categorized by skill category.

    Returns:
        Dict[category_name, List[canonical_skill_names]]
    """
    if not text:
        return {cat: [] for cat in SKILL_CATEGORIES}

    extracted_by_cat: Dict[str, Set[str]] = {cat: set() for cat in SKILL_CATEGORIES}
    seen_canonical: Set[str] = set()

    for cat, skill_list in SKILL_CATEGORIES.items():
        for skill in skill_list:
            canonical = normalize_skill(skill)
            pattern = _build_skill_regex(skill)
            if pattern.search(text):
                extracted_by_cat[cat].add(canonical)
                seen_canonical.add(canonical)

    # Convert sets to sorted lists
    return {cat: sorted(list(skills)) for cat, skills in extracted_by_cat.items()}


def extract_flat_skills(text: str) -> List[str]:
    """Extracts a flat sorted list of unique canonical skills found in text."""
    categorized = extract_skills(text)
    flat_skills: Set[str] = set()
    for cat_skills in categorized.values():
        flat_skills.update(cat_skills)
    return sorted(list(flat_skills))


def count_skill_frequencies(text: str, skills_to_check: List[str]) -> Dict[str, int]:
    """Counts occurrence frequencies of specified skills in text."""
    frequencies: Dict[str, int] = {}
    for skill in skills_to_check:
        canonical = normalize_skill(skill)
        pattern = _build_skill_regex(skill)
        matches = pattern.findall(text)
        frequencies[canonical] = len(matches)
    return frequencies
