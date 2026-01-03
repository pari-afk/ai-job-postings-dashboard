# AI Job Postings Dashboard

## Overview
This project analyzes AI and Data Science job postings from 2025 to identify role demand, required skills, and geographic hiring patterns. The primary objective is to transform raw job listing data into clear, interpretable insights that reflect current expectations in the AI job market.
The project emphasizes data cleaning, feature engineering, and exploratory analysis, with a dashboard-style presentation of results through visualizations.

The dataset used consists of AI and Data Science job postings collected from online job platforms. 
- Source: Kaggle (Data Science Job Market 2025)
- Time period: 2025 
- Format: CSV
- Size: ~900 job postings

The attributes include job title, seniority level, company, location and work mode (remote/hybrid/on-site), required skills, salary information

---

## Methods
The following machine learning techniques were applied:

### Data Cleaning & Feature Engineering
- Removing duplicate job postings
- Normalizing job titles and grouping them into role categories
- Standardizing seniority levels
- Parsing and cleaning skill lists into structured formats
- Extracting work mode (remote / hybrid / on-site) from location text
- Parsing salary ranges and currencies where possible
- Creating derived features such as:
    - Number of skills per posting
    - Primary job location
    -Skill presence indicators (e.g., Python, SQL, cloud tools)

### Exploratory Data Analysis
- Distribution of AI and Data Science job roles
- Most frequently requested technical skills
- Work mode distribution across postings
- Geographic concentration of job opportunities
- Differences in skill requirements across roles

---

## Key Results
- A small number of roles, such as Data Scientist and Machine Learning Engineer, account for a large share of AI-related job postings.
- Skills like Python, SQL, and machine learning frameworks appear most frequently across roles.
- Job postings show a strong presence of remote and hybrid roles, though on-site positions remain common.
- Hiring demand is concentrated in a limited number of geographic locations, reflecting centralized AI hiring hubs.
- More specialized roles tend to list a higher average number of required skills.

---

## Limitations
- The dataset represents a snapshot of job postings from 2025 rather than long-term trends.
- Job postings may not fully reflect actual hiring outcomes.
- Skill extraction relies on text fields and may miss implicit or unlisted requirements.
- Salary data is incomplete and varies in formatting.

---

## Repository Structure

ai-job-postings-dashboard/
├── data/
│   ├── raw/
│   │   └── data_science_job_posts_2025.csv
│   └── processed/
│       └── ai_jobs_clean.csv
├── figures/
│   ├── top_roles.png
│   ├── top_skills.png
│   ├── work_mode_distribution.png
│   ├── top_locations.png
│   └── skills_by_role.png
├── src/
│   ├── 01_clean.py
│   └── 02_eda.py
├── requirements.txt
└── README.md

---

## How to Run
1. Install dependencies:
pip install -r requirements.txt

2. Run data cleaning:
python src/01_clean.py

3. Run exploratory analysis
python src/02_eda.py

---

## Tech Stack
- Python
- pandas
- NumPy
- matplotlib

---

## Future Improvements
- Multi-year trend analysis using historical job postings
- Salary-focused analysis with standardized compensation metrics
- Skill co-occurrence and role similarity analysis
- Interactive dashboard implementation using tools such as Streamlit or Plotly
