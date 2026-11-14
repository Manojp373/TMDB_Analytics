# TMDB_Analytics
# 🎬 TMDB Movie Data Analysis & Insights Dashboard

An end-to-end **Movie Data Analysis and Visualization Project** built using Python, Pandas, SQL, Matplotlib, Seaborn, and Streamlit.

This project explores movie industry data to uncover meaningful insights about movie performance, genres, actors, directors, budgets, revenue, ratings, and audience popularity through data analysis and an interactive dashboard.

## 📌 Project Overview

The objective of this project is to transform raw movie datasets into meaningful insights using data cleaning, exploratory data analysis, SQL queries, and interactive visualizations.

The project follows a complete data analytics workflow, starting from raw data preparation and ending with an interactive Streamlit dashboard where users can explore movie insights through filters, charts, and analytical queries.

## 🎯 Key Features

### 1. Data Cleaning & Preprocessing
- Cleaned and prepared raw TMDB movie datasets using Python and Pandas.
- Handled missing values and inconsistent data.
- Processed movie attributes and prepared datasets for analysis.
- Exported cleaned datasets for further analysis and database integration.

### 2. SQL Analysis
- Integrated cleaned datasets into a MySQL database.
- Created and executed SQL queries to extract meaningful movie insights.
- Analyzed movie genres, revenue, budgets, actors, directors, and keywords.
- Explored relationships between movie performance and other attributes.

### 3. Pandas Exploratory Data Analysis
Performed analysis using Pandas to identify:
- Movie distribution across release years.
- Budget, revenue, profit, and ROI.
- Runtime distribution and outliers.
- Genre-wise popularity and ratings.
- Actor performance and movie contributions.
- Relationships between popularity and vote counts.

### 4. Data Visualization
Created 13 visualizations using Matplotlib and Seaborn, covering:

**Univariate Analysis**
- Budget distribution.
- Runtime box plot.
- Vote average distribution.
- Number of movies per genre.

**Bivariate Analysis**
- Budget vs Revenue.
- Popularity vs Vote Count.
- Average Rating by Genre.
- Movies Released per Year.

**Multivariate Analysis**
- Correlation Heatmap.
- Pair Plot.
- Budget vs Revenue by Genre.
- Vote Average Distribution by Genre.
- Average Revenue by Genre and Release Decade.

### 5. Interactive Streamlit Dashboard

Developed an interactive web application with four main sections:

| Section | Description |
|---|---|
| Home | Project introduction and movie overview. |
| Dashboard | KPI cards, top 10 highest-grossing movies, genre distribution, budget vs revenue analysis, and automated insights. |
| Query Explorer | Execute and explore 10 predefined SQL queries with results, charts, and text insights. |
| Visualization | Explore all 13 data visualizations interactively. |

**Interactive Filters:**
- Genre
- Release Year
- Minimum Rating
- Language

The selected filters dynamically update the movie data displayed in the dashboard and visualization sections.

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Data Analysis | Pandas, NumPy |
| Database | MySQL |
| Data Visualization | Matplotlib, Seaborn |
| Web Application | Streamlit |
| UI Components | Streamlit Option Menu |
| Development Environment | Jupyter Notebook, VS Code |
| Version Control | Git, GitHub |

## 📂 Project Structure

```text
TMDB-Movie-Data-Analysis/
│
├── CLEANED_DATA/
│   ├── movies.csv
│   ├── genres.csv
│   ├── cast.csv
│   ├── crew.csv
│   ├── movie_genres.csv
│   └── movie_keywords.csv
│
├── 01_data_cleaning.ipynb
├── 02_sql_analysis.ipynb
├── 03_pandas_analysis.ipynb
├── 04_data_visualization.ipynb
│
├── app.py
├── README.md
└── requirements.txt
```

## ⚙️ Installation & Setup

Follow these steps to run the project locally.

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

```bash
cd TMDB-Movie-Data-Analysis
```

### Step 2: Install Required Libraries

```bash
pip install -r requirements.txt
```

### Step 3: Configure MySQL Database

- Install and start MySQL Server.
- Create a database named `tmdb`.
- Import the six cleaned CSV datasets into their corresponding MySQL tables:
  - movies
  - genres
  - cast
  - crew
  - movie_genres
  - movie_keywords
- Update the MySQL connection details in `app.py` according to your local MySQL configuration.

### Step 4: Run the Streamlit Application

```bash
streamlit run app.py
```

The application will open in your browser.

## 📊 Analytical Highlights

Some of the findings identified during the analysis include:

- 2016 had the highest number of movie releases, with 121 movies.
- Science Fiction had the highest average popularity among primary genres in the analysis.
- Popularity and vote count showed a positive correlation of approximately 0.36.
- Runtime outliers were identified using the Interquartile Range (IQR) method.
- Movie performance was explored through budget, revenue, profit, and ROI calculations.

*Note: These findings are based on the cleaned dataset used in this project.*

## 💡 What I Learned

Through this project, I gained practical experience in:

- Data cleaning and preprocessing.
- Exploratory Data Analysis (EDA).
- Writing SQL queries and working with relational databases.
- Data manipulation using Pandas.
- Univariate, bivariate, and multivariate data visualization.
- Building interactive dashboards using Streamlit.
- Integrating Python applications with MySQL.
- Organizing an end-to-end data analytics project.

## 🚀 Future Enhancements

- Deploy the Streamlit application online.
- Add advanced movie recommendation features.
- Integrate predictive analytics for revenue and movie performance.
- Improve dashboard interactivity and reporting capabilities.
