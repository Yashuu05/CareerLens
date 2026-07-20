# *Student Skill gap analyzer & Placement Prediction*

# **Problem Statement**: 
- College Students pursuing a degree often face challenges to identify their potential regarding skills, career and placement. They learn many skills but couldn’t determine the gap between their current skills and industry required skills. They often have doubts like if these skills are enough for placement or if I have necessary skills, what skills lack in myself, what should I do for placement?

---

# **Solution** : 
- This solution offers a platform for college students to solve their doubts and challenges about skills and placement using machine learning. 
- This project has 3 core functionalities : 
1. Skill Gap Analyzer 
2. Placement Prediction
3. Career Recommendation 

---

# **Outcomes** : 
1. Calculated Skill Gap (float value)
2. Placement probability (percentage)
3. Personalized roadmap and recommendation (large text)
How can I learn the required skills for placement according to the current skill level, skill gap, placement probability and academic performance broken down in smaller practical steps with timeline.

---

# **Benefits** : 
1. Students can have a basic level of understanding about their position relative to the industry requirement.
2. A personalized guide to crack the placement based on the prediction and data.
Clear their doubts about placement and skills.

---

# *Project Structure* 
Student Skill Gap Analyzer

```
├── Data Layer
│      ├── Raw data
│      ├── Processed data
│      ├── External datasets
│      └── Data Versioning
│
├── Data Engineering
│      ├── Validation
│      ├── Cleaning
│      ├── Feature Store
│      └── Feature Engineering
│
├── ML Pipeline
│      ├── Training
│      ├── Evaluation
│      ├── Hyperparameter tuning
│      ├── Model Registry
│      └── Explainability
│
├── Backend API
│      ├── Prediction API
│      ├── Recommendation API
│      └── Authentication
│
├── Frontend
│      ├── Dashboard
│      ├── Student Report
│      └── Admin Panel
│
├── Monitoring
│      ├── Logs
│      ├── Drift Detection
│      ├── Model Performance
│      └── Alerts
│
└── DevOps
       ├── Docker
       ├── CI/CD
       ├── Cloud Deployment
       └── Documentation
```

---

# **Teck Stack**
```
programming : Python
ML: scikit-learn, CatBoost, XGBoost, LightGBM
Data Validation: Pandera or Great Expectations
Data Versioning: DVC
Experiment Tracking: MLflow
Workflow Orchestration: Apache Airflow
API: FastAPI
Frontend: or HTML/CSS/JavaScript
Database: PostgreSQL (metadata) + MongoDB (student profiles)
Cache (optional): Redis
Authentication: JWT
Containerization: Docker + Docker Compose
CI/CD: GitHub Actions
Monitoring: Prometheus + Grafana
Drift Detection: Evidently AI
Explainability: SHAP
Code Quality: Black, Ruff, mypy, pre-commit
Testing: pytest
Cloud Deployment: Azure
```

---

# **Dataset** 

1. ## Placement Prediction 
- Dataset source : click here to view dataset
- Dataset Overview
    1. Records: 100,000 student profiles
    2. Features: 18 columns
    3. Target Variables:1 
    4. Format: CSV

### Feature Description: 
1. branch	Categorical:	Engineering branch (CSE, ECE, ME, CE, EE, IT, Chemical)
2. College_tier: College tier (Tier-1, Tier-2, Tier-3)
3. cgpa: Cumulative GPA on a 10-point scale
4. Backlogs: Number of backlogs/failed subjects
5. Coding_skills: Self/test assessed coding ability
6. Dsa_score: Data Structures & Algorithms proficiency
7. Aptitude_score: Aptitude test percentile score
8. communication_skills	: Verbal and written communication ability
9. ml_knowledge	: Machine learning knowledge score
10. System_design : System design ability score
11. Internships : Number of internships completed
12. projects_count	: Number of projects completed
13. Certifications : Number of relevant certifications
14. Hackathons : Number of hackathons participated in
15. Open_source_contributions : Open source contribution count
16. extracurriculars	Integer (0–3)	Extracurricular activity involvement

## 2. Skill Gap 
Sample : 
Generation: Synthetic

Format : csv

Datasets: will be declared soon.

---

# **Machine Learning**

### Binary Classification Algorithms : 
1. Logistic regression
3. Decision Tree 
4. Random Forest
5. LightGBM
6. XGBoost 

### Performance Metrics : 
- Accuracy score
- Recall
- Precision
- F1_score
- ROC_AUC score

### Concepts : 
1. Hyperparameter tuning ( using optuna )
2. Serialization ( using Pickle )
3. Versioning ( DVC )
4. Tracking ( MLflow )
5. Registration ( MLflow )
6. Monitoring ( Grafana )

---

### LLM Used : 

1. NLP : 
- Llama3.1:8b 
- Gemini 2.5 or 3.0 Flash

### Image reading: 
- llava 
- Gemini 2.5 or 3.0 flash
