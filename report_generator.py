"""
report_generator.py
-------------------
Generates downloadable analysis reports (Markdown/Text format)
for AI Resume Analyzer.
"""

from datetime import datetime
from typing import Any, Dict


def generate_text_report(analysis_results: Dict[str, Any], metadata: Dict[str, Any]) -> str:
    """
    Generates a structured plain text / Markdown report summarizing the resume analysis.

    Args:
        analysis_results: Dictionary output from analyzer.analyze_resume_vs_jd()
        metadata: PDF metadata dictionary (filename, num_pages, word_count, char_count)

    Returns:
        Formatted text string ready for download.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    score = analysis_results.get("match_score", 0)
    breakdown = analysis_results.get("score_breakdown", {})
    matched_skills = analysis_results.get("matched_skills", [])
    missing_skills = analysis_results.get("missing_skills", [])
    matched_kw = analysis_results.get("matched_keywords", [])
    missing_kw = analysis_results.get("missing_keywords", [])
    sections = analysis_results.get("sections_status", {})
    quality = analysis_results.get("quality_checks", [])
    recs = analysis_results.get("recommendations", [])
    jd_info = analysis_results.get("jd_info", {})

    lines = []
    lines.append("================================================================================")
    lines.append("                          AI RESUME ANALYZER REPORT                             ")
    lines.append("================================================================================")
    lines.append(f"Generated On   : {timestamp}")
    lines.append(f"Resume File    : {metadata.get('filename', 'Resume.pdf')}")
    lines.append(f"Page Count     : {metadata.get('num_pages', 1)}")
    lines.append(f"Word Count     : {metadata.get('word_count', 0)} words")
    lines.append("--------------------------------------------------------------------------------")
    lines.append("")

    # Overall Score & Status
    lines.append("--------------------------------------------------------------------------------")
    lines.append(f"1. OVERALL RESUME MATCH SCORE : {score} / 100")
    lines.append("--------------------------------------------------------------------------------")
    lines.append("Score Breakdown:")
    for key, data in breakdown.items():
        name = key.replace("_", " ").title()
        lines.append(f"  • {name:<20}: {data['score_pct']}% (Weight: {data['weight_pct']}%, Contributed: {data['contribution']} pts)")
    lines.append("")
    lines.append("Note: This match score is an automated estimate for guidance and optimization.")
    lines.append("It does not represent a formal hiring decision.")
    lines.append("")

    # Job Requirements Summary
    lines.append("--------------------------------------------------------------------------------")
    lines.append("2. JOB DESCRIPTION REQUIREMENTS SUMMARY")
    lines.append("--------------------------------------------------------------------------------")
    lines.append(f"Experience Required : {jd_info.get('experience_requirement', 'N/A')}")
    lines.append(f"Education Required  : {jd_info.get('education_requirement', 'N/A')}")
    lines.append(f"Total Skills in JD  : {len(analysis_results.get('jd_skills', []))}")
    lines.append("")

    # Skills Breakdown
    lines.append("--------------------------------------------------------------------------------")
    lines.append("3. SKILLS ANALYSIS")
    lines.append("--------------------------------------------------------------------------------")
    lines.append(f"Skill Match Summary: {len(matched_skills)} / {len(analysis_results.get('jd_skills', []))} skills matched")
    lines.append("")
    lines.append("Matching Skills You Have:")
    if matched_skills:
        for s in matched_skills:
            lines.append(f"  [✓] {s}")
    else:
        lines.append("  (No direct technical skill matches found)")

    lines.append("")
    lines.append("Skills You May Be Missing (Sorted by Frequency/Relevance in JD):")
    if missing_skills:
        for s in missing_skills:
            freq = jd_info.get('skill_frequencies', {}).get(s, 1)
            lines.append(f"  [✗] {s} (Mentioned {freq}x in JD)")
    else:
        lines.append("  (None! You match all skills mentioned in the JD.)")
    lines.append("")

    # Keyword Analysis
    lines.append("--------------------------------------------------------------------------------")
    lines.append("4. KEYWORD MATCH ANALYSIS")
    lines.append("--------------------------------------------------------------------------------")
    lines.append("Matched Important Terms:")
    if matched_kw:
        lines.append("  " + ", ".join(matched_kw))
    else:
        lines.append("  (None)")
    
    lines.append("")
    lines.append("Missing Important Terms:")
    if missing_kw:
        lines.append("  " + ", ".join(missing_kw))
    else:
        lines.append("  (None)")
    lines.append("")

    # Resume Structure Check
    lines.append("--------------------------------------------------------------------------------")
    lines.append("5. RESUME STRUCTURE AUDIT")
    lines.append("--------------------------------------------------------------------------------")
    for sec_name, status in sections.items():
        symbol = "[✓] Present" if status else "[✗] Missing"
        lines.append(f"  {symbol:<15} : {sec_name}")
    lines.append("")

    # Quality Check
    lines.append("--------------------------------------------------------------------------------")
    lines.append("6. RESUME QUALITY AUDIT")
    lines.append("--------------------------------------------------------------------------------")
    for item in quality:
        symbol = "[GOOD]" if item["type"] == "good" else "[ATTENTION]"
        lines.append(f"  {symbol} {item['title']}: {item['description']}")
        if item.get("example"):
            lines.append(f"    Suggestion: {item['example']}")
    lines.append("")

    # Recommendations
    lines.append("--------------------------------------------------------------------------------")
    lines.append("7. RECOMMENDATIONS TO IMPROVE MATCH SCORE")
    lines.append("--------------------------------------------------------------------------------")
    for idx, rec in enumerate(recs, 1):
        clean_rec = rec.replace("**", "").replace("⚠️ ", "")
        lines.append(f"  {idx}. {clean_rec}")
    lines.append("")
    lines.append("================================================================================")
    lines.append("                           END OF ANALYSIS REPORT                               ")
    lines.append("================================================================================")

    return "\n".join(lines)
