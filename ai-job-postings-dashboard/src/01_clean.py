import os
import re
import ast
import pandas as pd
import numpy as np

#project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(PROJECT_ROOT)

raw_path = "data/raw/data_science_job_posts_2025.csv"
out_path = "data/processed/ai_jobs_clean.csv"

os.makedirs("data/processed", exist_ok=True)

print("Current working directory:", os.getcwd())
print("Raw file exists?", os.path.exists(raw_path))

def safe_list_parse(x):
    if pd.isna(x):
        return []
    if isinstance(x, list):
        return [str(i).strip().lower() for i in x if str(i).strip()]
    s = str(x).strip()
    if s == "" or s == "[]":
        return []
    try:
        parsed = ast.literal_eval(s)
        if isinstance(parsed, list):
            return [str(i).strip().lower() for i in parsed if str(i).strip()]
        return []
    except Exception:
        s = s.strip("[]")
        parts = [p.strip(" '\"").lower() for p in s.split(",")]
        return [p for p in parts if p]

def normalize_title(title):
    if pd.isna(title):
        return ""
    t = str(title).lower().strip()
    t = re.sub(r"\s+", " ", t)
    return t

def categorize_role(title_norm):
    t = title_norm

    if any(k in t for k in ["machine learning engineer", "ml engineer", "mle"]):
        return "Machine Learning Engineer"
    if any(k in t for k in ["data engineer"]):
        return "Data Engineer"
    if any(k in t for k in ["data analyst", "analytics analyst", "business analyst"]):
        return "Data Analyst"
    if any(k in t for k in ["research scientist", "applied scientist", "researcher"]):
        return "Research Scientist"
    if any(k in t for k in ["ai engineer", "artificial intelligence", "ai specialist"]):
        return "AI Engineer"
    if any(k in t for k in ["deep learning"]):
        return "Deep Learning"
    if any(k in t for k in ["computer vision"]):
        return "Computer Vision"
    if any(k in t for k in ["nlp", "natural language"]):
        return "NLP"
    if any(k in t for k in ["data scientist", "datascientist"]):
        return "Data Scientist"
    if any(k in t for k in ["statistician"]):
        return "Statistician"

    return "Other"

def normalize_seniority(x):
    if pd.isna(x):
        return "Unknown"
    s = str(x).lower().strip()

    if s in ["intern", "internship"]:
        return "Intern"
    if s in ["junior", "entry", "entry level", "associate"]:
        return "Junior"
    if s in ["mid", "mid level", "intermediate"]:
        return "Mid"
    if s in ["senior", "sr"]:
        return "Senior"
    if s in ["lead", "principal", "staff"]:
        return "Lead"
    if s in ["manager", "head"]:
        return "Manager"
    if s in ["director", "vp", "vice president"]:
        return "Director+"

    return s.title()

def parse_work_mode(location_str):
    if pd.isna(location_str):
        return "Unknown"
    s = str(location_str).lower()
    if "remote" in s:
        return "Remote"
    if "hybrid" in s:
        return "Hybrid"
    if "on-site" in s or "onsite" in s:
        return "On-site"
    return "Unknown"

def extract_locations(location_str):
    if pd.isna(location_str):
        return []
    raw = str(location_str).strip()
    parts = [p.strip() for p in raw.split(" . ") if p.strip()]

    cleaned = []
    for p in parts:
        lp = p.lower()
        if lp in ["remote", "hybrid", "on-site", "onsite"]:
            continue
        cleaned.append(p)

        return cleaned

def parse_days_ago(post_date):
    if pd.isna(post_date):
        return np.nan
    s = str(post_date).lower().strip()

    if s == "today":
        return 0
    if "day" in s:
        m = re.search(r"(\d+)", s)
        return int(m.group(1)) if m else np.nan
    if "week" in s:
        m = re.search(r"(\d+)", s)
        return int(m.group(1)) * 7 if m else 7
    if "month" in s:
        m = re.search(r"(\d+)", s)
        return int(m.group(1)) * 30 if m else 30

    return np.nan

def parse_salary(salary_str):
    if pd.isna(salary_str):
        return ("Unknown", np.nan, np.nan)

    s = str(salary_str).strip()
    if s == "":
        return ("Unknown", np.nan, np.nan)

    currency = "Unknown"
    if "€" in s:
        currency = "EUR"
    elif "$" in s:
        currency = "USD"
    elif "£" in s:
        currency = "GBP"
    elif "cad" in s.lower():
        currency = "CAD"
                    

        nums = re.findall(r"\d[\d,]*", s)
        nums = [int(n.replace(",", "")) for n in nums] if nums else []

        if len(nums) == 0:
            return (currency, np.nan, np.nan)
        if len(nums) == 1:
            return (currenct, nums[0], nums[0])
        return (currency, min(nums), max(nums))

df = pd.read_csv(raw_path)

print("Loaded rows:", len(df))
print("Columns:", list(df.columns))

for col in ["job_title", "company", "location", "seniority_level", "status"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

df = df.drop_duplicates()

df["job_title_norm"] = df["job_title"].apply(normalize_title)
df["role_category"] = df["job_title_norm"].apply(categorize_role)

df["seniority_clean"] = df["seniority_level"].apply(normalize_seniority)

df["work_mode"] = df["location"].apply(parse_work_mode)
df["location_list"] = df["location"].apply(extract_locations)
df["primary_location"] = df["location_list"].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else "Unknown")

df["days_ago"] = df["post_date"].apply(parse_days_ago)

salary_parsed = df["salary"].apply(lambda s: parse_salary(s) or ("Unknown", np.nan, np.nan))
df["salary_currency"] = salary_parsed.apply(lambda x: x[0])
df["salary_min"] = salary_parsed.apply(lambda x: x[1])
df["salary_max"] = salary_parsed.apply(lambda x: x[2])


df["skills_list"] = df["skills"].apply(safe_list_parse)
df["num_skills"] = df["skills_list"].apply(len)

key_skills = [
    "python", "sql", "r",
    "excel", "tableau", "power bi",
    "aws", "azure", "gcp",
    "spark", "docker", "kubernetes",
    "tensorflow", "pytorch",
    "scikit-learn", "pandas"
]

for sk in key_skills:
    colname = f"has_{sk.replace('-', '_').replace(' ', '_')}"
    df[colname] = df["skills_list"].apply(lambda lst: sk in lst)

df = df[df["job_title_norm"] != ""]

df.to_csv(out_path, index=False)

print("Cleaning complete")
print("Rows kept:", len(df))
print("Saved to:", out_path)

