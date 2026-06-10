from pathlib import Path
import re
import pandas as pd

# This is the spreadsheet you created from real job research
file_path = Path("ai_career_real_jobs_tracker.xlsx")

if not file_path.exists():
    raise FileNotFoundError("Spreadsheet not found. Make sure ai_career_real_jobs_tracker.xlsx is in this folder.")

# Read the Job Tracker sheet from the Excel file
df = pd.read_excel(file_path, sheet_name="Job Tracker")

print("\nSpreadsheet loaded successfully.")
print("Number of job rows found:", len(df))

print("\nFirst few jobs:")
print(df.head().to_string(index=False))

# These are the skills/tools we want to search for inside the job data
skill_patterns = {
    "Python": r"\bpython\b",
    "SQL": r"\bsql\b",
    "Excel": r"\bexcel\b",
    "Power BI": r"\bpower\s*bi\b",
    "Tableau": r"\btableau\b",
    "Git": r"\bgit\b|\bgithub\b",
    "Linux": r"\blinux\b",
    "APIs": r"\bapi\b|\bapis\b|\brest\b",
    "Docker": r"\bdocker\b",
    "Kubernetes": r"\bkubernetes\b|\bk8s\b",
    "Azure": r"\bazure\b",
    "AWS": r"\baws\b|amazon web services",
    "Cloud": r"\bcloud\b",
    "Machine Learning": r"machine learning|\bml\b",
    "LLMs": r"\bllm\b|\bllms\b|large language model",
    "RAG": r"\brag\b|retrieval augmented generation",
    "LangChain": r"\blangchain\b",
    "Hugging Face": r"hugging face",
    "OpenAI": r"\bopenai\b",
    "FastAPI": r"\bfastapi\b",
    "Flask": r"\bflask\b",
    "JavaScript": r"\bjavascript\b|\bjs\b",
    "TypeScript": r"\btypescript\b|\bts\b",
    "React": r"\breact\b",
    "CI/CD": r"\bci/cd\b|\bcontinuous integration\b|\bcontinuous deployment\b",
    "Testing": r"\btesting\b|\bunit test\b|\bqa\b",
    "ETL": r"\betl\b|data pipeline|data pipelines",
    "Spark": r"\bspark\b",
    "Databricks": r"\bdatabricks\b",
    "Cybersecurity": r"cybersecurity|security",
    "SIEM": r"\bsiem\b",
    "Incident Response": r"incident response",
    "Vulnerability Management": r"vulnerability",
    "IAM": r"\biam\b|identity and access",
    "Troubleshooting": r"troubleshooting|debugging",
    "Microsoft 365": r"microsoft 365|office 365|m365",
    "Documentation": r"documentation|documenting|write-up|writeups",
    "Communication": r"communication|stakeholder|client|customer",
    "Automation": r"automation|automate",
    "AI Agents": r"agent|agents|agentic",
    "Observability": r"observability|monitoring|logging|logs"
}

# Join each row into one text block, then check which skills appear in that row
results = []

for skill, pattern in skill_patterns.items():
    count = 0

    for _, row in df.iterrows():
        row_text = " ".join(str(value) for value in row.values if pd.notna(value))

        if re.search(pattern, row_text, flags=re.IGNORECASE):
            count += 1

    if count > 0:
        results.append({
            "Skill or Tool": skill,
            "Number of Job Rows Mentioning It": count
        })

summary = pd.DataFrame(results)
summary = summary.sort_values(by="Number of Job Rows Mentioning It", ascending=False)

print("\nTop repeated skills/tools:")
print(summary.head(20).to_string(index=False))

# Save the results
summary.to_csv("top_skills_report.csv", index=False)

with open("top_skills_report.txt", "w", encoding="utf-8") as f:
    f.write("Top repeated skills/tools from AI career job tracker\n")
    f.write("=" * 55 + "\n\n")
    f.write(summary.to_string(index=False))

print("\nDone.")
print("Created: top_skills_report.csv")
print("Created: top_skills_report.txt")
