import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

#project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(PROJECT_ROOT)

in_path = "data/processed/ai_jobs_clean.csv"
fig_dir = "figures"
os.makedirs(fig_dir, exist_ok=True)

print("Current working directory:", os.getcwd())
print("File exists?", os.path.exists(in_path))

#loading data
df = pd.read_csv(in_path)
print("Loaded shape:", df.shape)

#top job roles
role_counts = (
    df["role_category"]
    .value_counts()
    .head(10)
)

plt.figure()
role_counts.plot(kind="bar")
plt.title("Top AI & Data Job Roles")
plt.xlabel("Role")
plt.ylabel("Number of Postings")
plt.tight_layout()
plt.savefig(f"{fig_dir}/top_roles.png", dpi=200)
plt.close()

#top skills
all_skills = []
for skills in df["skills_list"]:
    if isinstance(skills, str):
        skills = eval(skills)
        all_skills.extend(skills)

skill_counts = Counter(all_skills)
top_skills = dict(skill_counts.most_common(15))

plt.figure()
plt.bar(top_skills.keys(), top_skills.values())
plt.title("Top 15 In-Demand Skills")
plt.xlabel("Skill")
plt.ylabel("Frequency")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(f"{fig_dir}/top_skills.png", dpi=200)
plt.close()

#work mode distribution
work_mode_counts = df["work_mode"].value_counts()

plt.figure()
work_mode_counts.plot(kind="bar")
plt.title("Work Mode Distribution")
plt.xlabel("Work Mode")
plt.ylabel("Number of Postings")
plt.tight_layout()
plt.savefig(f"{fig_dir}/work_mode_distribution.png", dpi=200)
plt.close()

#top locations
location_counts = (
    df["primary_location"]
    .value_counts()
    .head(10)
)

plt.figure()
location_counts.plot(kind="bar")
plt.title("Top Job Locations")
plt.xlabel("Location")
plt.ylabel("Number of Postings")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(f"{fig_dir}/top_locations.png", dpi=200)
plt.close()

#average number of skills by role
skills_by_role = (
    df.groupby("role_category")["num_skills"]
    .mean()
    .sort_values(ascending=False)
)

plt.figure()
skills_by_role.plot(kind="bar")
plt.title("Average Number of Skills Required by Role")
plt.xlabel("Role")
plt.ylabel("Average Skill Count")
plt.tight_layout()
plt.savefig(f"{fig_dir}/skills_by_role.png", dpi=200)
plt.close()

print("EDA complete")
print("Figures saved to:", fig_dir)
