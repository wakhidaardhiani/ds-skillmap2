# SkillMap Career: AI Career Recommendation Dashboard

SkillMap Career is an AI-powered career recommendation dashboard developed using **Streamlit**, **Python**, and **Machine Learning**. The platform helps students and graduates explore suitable career paths by analyzing their academic background, interests, skills, certifications, work preferences, and experiences.

Through interactive visualizations, exploratory data analysis (EDA), and career recommendation insights, users can gain valuable information to support data-driven career planning and decision-making.

## Live Demo

Dashboard: https://skillmapcarrier.streamlit.app/

---

## Project Objectives

* Analyze student academic and professional profiles.
* Explore relationships between skills, interests, experiences, and career recommendations.
* Provide interactive visualizations for career-related insights.
* Support data-driven career planning through AI-based recommendations.
* Demonstrate the implementation of Data Analytics and Machine Learning in career guidance systems.

---

## Key Features

### Home Dashboard

* Executive overview of the dataset
* KPI cards and summary statistics
* Dataset preview and quick insights

### Data Overview

* Interactive data table
* Dataset structure information
* Data types analysis
* Missing value detection

### Exploratory Data Analysis (EDA)

* Distribution of majors, interests, and career goals
* Histogram analysis
* Pie chart visualizations
* Correlation heatmap
* Interactive Plotly charts

### Career Insights

* Top recommended careers
* Career trends and patterns
* Academic performance vs career recommendations
* Internship and certification analysis

### Interactive Filtering

* Filter by major, interests, work style, and career goals
* Search functionality
* Download filtered dataset
* Dynamic statistics update

---

## 🛠️ Technology Stack

| Category             | Technology                |
| -------------------- | ------------------------- |
| Programming Language | Python                    |
| Framework            | Streamlit                 |
| Data Processing      | Pandas, NumPy             |
| Visualization        | Plotly                    |
| Machine Learning     | Scikit-learn              |
| Deployment           | Streamlit Community Cloud |
| Version Control      | Git & GitHub              |

---

## Project Structure

```text
AI-Career-Recommendation-Dashboard/
│
├── streamlit_app.py
├── utils.py
├── requirements.txt
├── Career_Recommendation_Cleaned.csv
│
├── pages/
│   ├── home.py
│   ├── data_overview.py
│   ├── eda.py
│   ├── career_insights.py
│   └── filter_page.py
│
└── assets/
```

---

## Dataset Information

The dataset contains approximately **49,500 records** and **20 features** related to:

* Academic Major
* GPA (IPK)
* Areas of Interest
* Technical Skills
* Leadership
* Communication Skills
* Teamwork
* Creativity
* Critical Thinking
* Problem Solving
* Internship Experience
* Organizational Experience
* Competition Experience
* Certifications
* Work Style Preferences
* Industry Preferences
* Career Goals
* Career Recommendations

---

## Installation & Usage

### 1. Clone Repository

```bash
git clone https://github.com/your-username/AI-Career-Recommendation-Dashboard.git
cd AI-Career-Recommendation-Dashboard
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Application

```bash
streamlit run streamlit_app.py
```

### 4. Open Dashboard

```text
http://localhost:8501
```

---

## Dashboard Preview

You can access the live application here:

https://skillmapcarrier.streamlit.app/

---

## Future Improvements

* Career Prediction using Machine Learning
* Personalized Recommendation System
* User Authentication
* Export Reports (PDF/Excel)
* Advanced Analytics Dashboard
* AI Chat Assistant for Career Guidance

---

