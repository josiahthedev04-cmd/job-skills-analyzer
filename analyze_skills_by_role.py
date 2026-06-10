from pathlib import Path
import re
import pandas as pd

file_path = Path("ai_career_real_jobs_tracker.xlsx")

if not file_path.exists():
    raise FileNotFoundError("ai_career_real_jobs_tracker.xlsx was not found.")

df = pd.read_excel(file_path, sheet_name="Job Tracker")

# Find the job title column automatically
possible_role_columns = ["Job Title", "Target Role", "Role", "Role Family", "Job Role"]
role_column = None

for col in possible_role_columns:
    if col in df.columns:
        role_column = col
        break

if role_column is None:
    raise ValueError("Could not find a role/job title column. Check your spreadsheet column names.")

skill_patterns = {
    "Python": r"\bpython\b",
    "Git": r"\bgit\b|\bgithub\b",
    "Cybersecurity": r"cybersecurity|security",
    "APIs": r"\bapi\b|\bapis\b|\brest\b",
    "Cloud": r"\bcloud\b|\baws\b|\bazure\b|google cloud",
    "Docker": r"\bdocker\b",
    "SQL": r"\bsql\b",
    "Documentation": r"documentation|documenting|write-up|writeups",
    "Communication": r"communication|stakeholder|client|customer",
    "LLMs": r"\bllm\b|\bllms\b|large language model",
    "Linux": r"\blinux\b",
    "RAG": r"\brag\b|retrieval augmented generation",
    "Troubleshooting": r"troubleshooting|debugging",
    "AI Agents": r"agent|agents|agentic",
    "Machine Learning": r"machine learning|\bml\b",
    "Power BI": r"\bpower\s*bi\b",
    "Excel": r"\bexcel\b",
    "Azure": r"\bazure\b",
    "AWS": r"\baws\b|amazon web services",
    "Tableau": r"\btableau\b",
    "Databricks": r"\bdatabricks\b",
    "Spark": r"\bspark\b",
    "ETL": r"\betl\b|data pipeline|data pipelines",
    "Testing": r"\btesting\b|\bunit test\b|\bqa\b",
    "CI/CD": r"\bci/cd\b|\bcontinuous integration\b|\bcontinuous deployment\b",
    "FastAPI": r"\bfastapi\b",
    "IAM": r"\biam\b|identity and access",
    "Automation": r"automation|automate",
    "Observability": r"observability|monitoring|logging|logs"
}

rows = []

for _, job in df.iterrows():
    role = str(job.get(role_column, "Unknown Role"))

    row_text = " ".join(str(value) for value in job.values if pd.notna(value))

    for skill, pattern in skill_patterns.items():
        if re.search(pattern, row_text, flags=re.IGNORECASE):
            rows.append({
                "Role": role,
                "Skill or Tool": skill
            })

role_skill_df = pd.DataFrame(rows)

if role_skill_df.empty:
    raise ValueError("No skills were detected. Check the spreadsheet content.")

summary = (
    role_skill_df
    .groupby(["Role", "Skill or Tool"])
    .size()
    .reset_index(name="Mentions")
    .sort_values(["Role", "Mentions"], ascending=[True, False])
)

summary.to_csv("role_by_role_skill_report.csv", index=False)

with open("role_by_role_skill_report.txt", "w", encoding="utf-8") as f:
    f.write("Role-by-role skill report\n")
    f.write("=" * 35 + "\n\n")

    for role in summary["Role"].unique():
        f.write(f"{role}\n")
        f.write("-" * len(role) + "\n")

        role_rows = summary[summary["Role"] == role].head(10)

        for _, row in role_rows.iterrows():
            f.write(f"- {row['Skill or Tool']}: {row['Mentions']}\n")

        f.write("\n")

print("Done.")
print("Created: role_by_role_skill_report.csv")
print("Created: role_by_role_skill_report.txt")
