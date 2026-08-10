# 🎓 EduPro – Instructor Performance & Course Quality Evaluation

## 📌 Project Overview

EduPro is an online education platform where instructor effectiveness and course quality play an important role in learner satisfaction and platform credibility.

This project develops a data-driven framework to evaluate instructor performance, course quality, teaching experience, expertise, and enrollment behavior.

The project includes Exploratory Data Analysis (EDA), KPI analysis, data integration, and an interactive Streamlit dashboard.

---

## 🎯 Problem Statement

EduPro currently lacks a structured and data-driven framework for evaluating instructor performance and course quality.

The project aims to answer:

- Which instructors consistently deliver high-quality courses?
- Does teaching experience translate into better ratings?
- Is there a relationship between instructor ratings and course ratings?
- Which expertise areas deliver the highest course quality?
- Are highly rated instructors associated with higher enrollments?
- How evenly is teaching performance distributed across the platform?

---

## 🎯 Project Objectives

- Analyze instructor performance and ratings.
- Evaluate course quality across categories and levels.
- Study the relationship between teaching experience and instructor ratings.
- Analyze the relationship between TeacherRating and CourseRating.
- Compare instructor rating tiers and enrollment activity.
- Identify expertise-wise performance patterns.
- Develop KPIs for instructor and course evaluation.
- Build an interactive Streamlit dashboard.

---

## 📂 Dataset

The project uses four main datasets:

### Teachers
Contains:
- TeacherID
- Expertise
- YearsOfExperience
- TeacherRating

### Courses
Contains:
- CourseID
- CourseCategory
- CourseType
- CourseLevel
- CoursePrice
- CourseDuration
- CourseRating
- TeacherID

### Transactions
Contains:
- TransactionID
- UserID
- CourseID
- TransactionDate
- Amount

### Users
Contains:
- UserID
- Age
- Gender

The datasets were integrated using `TeacherID` and `CourseID`.

---

## 🔍 Analytical Methodology

The project follows these major stages:

1. Data Loading
2. Data Cleaning
3. Missing Value Analysis
4. Data Type Validation
5. Data Integration
6. Exploratory Data Analysis
7. Instructor Performance Analysis
8. Experience vs Rating Analysis
9. Course Quality Analysis
10. Expertise-wise Analysis
11. Enrollment Analysis
12. KPI Calculation
13. Streamlit Dashboard Development

---

## 📊 Key Performance Indicators

| KPI | Value |
|---|---:|
| Average Teacher Rating | 4.190 / 5 |
| Average Course Rating | 4.350 / 5 |
| Rating Consistency Index | 0.463 |
| Experience Impact Score | -0.256 |
| Enrollment Influence Ratio | 0.570 |

### KPI Interpretation

**Average Teacher Rating – 4.190**

Indicates an overall positive instructor-quality benchmark.

**Average Course Rating – 4.350**

Indicates that courses receive positive learner ratings overall.

**Rating Consistency Index – 0.463**

Shows measurable variation in instructor performance, highlighting the importance of monitoring individual instructors rather than relying only on platform averages.

**Experience Impact Score – -0.256**

Shows a negative observed relationship between experience and teacher rating in this dataset. This suggests that years of experience alone should not be considered a guarantee of teaching effectiveness.

**Enrollment Influence Ratio – 0.570**

Provides a comparison of enrollment activity across instructor rating tiers. Enrollment should be interpreted together with factors such as course availability, pricing, category, and promotion.

---

## 📈 Streamlit Dashboard

The project includes an interactive Streamlit dashboard with:

### 🏆 Instructor Performance
- Instructor leaderboard
- Teacher rating analysis
- Experience vs rating scatter plot
- Enrollment by instructor rating tier

### 📚 Course Quality
- Course rating by category
- Course rating by level
- Category × Level heatmap

### 🎯 Expertise Analysis
- Expertise-wise performance comparison
- Teacher rating vs course rating
- Enrollment comparison

### 🔎 Interactive Filters
- Instructor expertise
- Course category
- Course level
- Teacher rating range

### 💡 Insights & Recommendations
The dashboard provides data-driven findings and recommendations for improving instructor and course quality.

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- Jupyter Notebook
- VS Code

---

## 📁 Project Structure

```text
EduPro-Instructor-Performance-Analysis/
│
├── app.py
├── code.ipynb
├── edupro_final_data.csv
├── edupro_teachers.csv
├── edupro_courses.csv
├── edupro_transactions.csv
├── edupro_users.csv
├── requirements.txt
└── README.md
