import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

csv_path = Path("top_skills_report.csv")

if not csv_path.exists():
    raise FileNotFoundError("top_skills_report.csv was not found. Run analyze_job_skills.py first.")

df = pd.read_csv(csv_path)

# Use the top 15 skills so the chart stays readable
df = df.sort_values("Number of Job Rows Mentioning It", ascending=False).head(15)

# Reverse so the highest value appears at the top in a horizontal chart
chart_df = df.iloc[::-1]

plt.figure(figsize=(10, 7))
plt.barh(chart_df["Skill or Tool"], chart_df["Number of Job Rows Mentioning It"])

plt.title("Top Repeated Skills From AI and IT Job Postings")
plt.xlabel("Number of Job Rows Mentioning Skill")
plt.ylabel("Skill or Tool")

# Add the number at the end of each bar
for index, value in enumerate(chart_df["Number of Job Rows Mentioning It"]):
    plt.text(value + 0.1, index, str(value), va="center")

plt.tight_layout()
plt.savefig("top_skills_chart.png", dpi=200)

print("Chart created: top_skills_chart.png")
