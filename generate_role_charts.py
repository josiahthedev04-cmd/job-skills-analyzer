from pathlib import Path
import re
import pandas as pd
import matplotlib.pyplot as plt

report_path = Path("role_by_role_skill_report.csv")
charts_dir = Path("charts_by_role")

if not report_path.exists():
    raise FileNotFoundError("role_by_role_skill_report.csv was not found. Run analyze_skills_by_role.py first.")

charts_dir.mkdir(exist_ok=True)

df = pd.read_csv(report_path)

required_columns = {"Role", "Skill or Tool", "Mentions"}
missing_columns = required_columns - set(df.columns)

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

def clean_filename(text):
    text = str(text).lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = text.strip("_")
    return text or "unknown_role"

generated_charts = []

for role in sorted(df["Role"].dropna().unique()):
    role_df = df[df["Role"] == role].copy()
    role_df = role_df.sort_values("Mentions", ascending=False).head(10)

    if role_df.empty:
        continue

    # Reverse so the highest value appears at the top of the horizontal chart
    chart_df = role_df.iloc[::-1]

    safe_name = clean_filename(role)
    chart_path = charts_dir / f"{safe_name}_top_skills.png"

    plt.figure(figsize=(10, 6))
    plt.barh(chart_df["Skill or Tool"], chart_df["Mentions"])
    plt.title(f"Top Skills for {role}")
    plt.xlabel("Mentions")
    plt.ylabel("Skill or Tool")

    for index, value in enumerate(chart_df["Mentions"]):
        plt.text(value + 0.05, index, str(value), va="center")

    plt.tight_layout()
    plt.savefig(chart_path, dpi=200)
    plt.close()

    generated_charts.append((role, chart_path.as_posix()))

print("Role-by-role charts created:")
for role, path in generated_charts:
    print(f"- {role}: {path}")

# Create a markdown section that can be added to README.md
section_lines = []
section_lines.append("## Role-by-Role Charts")
section_lines.append("")
section_lines.append("The charts below show the top skills detected for each job role in the tracker.")
section_lines.append("")

for role, path in generated_charts:
    section_lines.append(f"### {role}")
    section_lines.append("")
    section_lines.append(f"![Top Skills for {role}]({path})")
    section_lines.append("")

new_section = "\n".join(section_lines)

readme_path = Path("README.md")

if readme_path.exists():
    readme = readme_path.read_text(encoding="utf-8")
else:
    readme = "# Job Skills Analyzer\n"

start_marker = "<!-- ROLE_CHARTS_START -->"
end_marker = "<!-- ROLE_CHARTS_END -->"

wrapped_section = f"{start_marker}\n\n{new_section}\n\n{end_marker}"

if start_marker in readme and end_marker in readme:
    before = readme.split(start_marker)[0].rstrip()
    after = readme.split(end_marker)[1].lstrip()
    updated_readme = f"{before}\n\n{wrapped_section}\n\n{after}"
else:
    updated_readme = readme.rstrip() + "\n\n" + wrapped_section + "\n"

readme_path.write_text(updated_readme, encoding="utf-8")

print("")
print("README.md updated with role-by-role chart section.")
