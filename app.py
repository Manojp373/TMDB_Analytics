import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="TMDB Movie Insights",
    page_icon="🎬",
    layout="wide"
)


st.markdown("""
<style>

/* MAIN APP BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #080808, #141414, #080808);
    color: #F5F5F5;
}

/* MAIN CONTENT */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* HEADINGS */
h1, h2, h3 {
    color: #F5C542 !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px;
}

/* NORMAL TEXT */
p, label, span {
    color: #E5E5E5;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111111, #1B1B1B);
    border-right: 1px solid #B8860B;
}

/* SIDEBAR HEADINGS */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #F5C542 !important;
}

/* METRIC CARDS */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #242424, #111111);
    border: 1px solid #8C6A12;
    border-left: 4px solid #F5C542;
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0 5px 18px rgba(245, 197, 66, 0.12);
}

/* METRIC LABEL */
div[data-testid="stMetricLabel"] {
    color: #D6B85A !important;
}

/* METRIC VALUE */
div[data-testid="stMetricValue"] {
    color: #FFD95A !important;
    font-weight: 700;
}

/* SELECTBOX AND MULTISELECT */
div[data-baseweb="select"] > div {
    background-color: #222222 !important;
    border: 1px solid #8C6A12 !important;
    border-radius: 8px !important;
    color: #FFD95A !important;
}

/* INPUT BOXES */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background-color: #202020 !important;
    color: #FFD95A !important;
    border: 1px solid #8C6A12 !important;
    border-radius: 8px !important;
}

/* BUTTONS */
.stButton > button {
    background: linear-gradient(135deg, #F5C542, #B8860B);
    color: #111111 !important;
    border: none;
    border-radius: 9px;
    font-weight: 700;
    transition: 0.3s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #FFE082, #F5C542);
    color: #000000 !important;
    box-shadow: 0 0 15px rgba(245, 197, 66, 0.4);
}

/* SLIDERS */
div[data-testid="stSlider"] [role="slider"] {
    background-color: #F5C542 !important;
}

/* DATAFRAMES */
div[data-testid="stDataFrame"] {
    border: 1px solid #8C6A12;
    border-radius: 10px;
    overflow: hidden;
}

/* INSIGHT BOXES */
div[data-testid="stAlert"] {
    background-color: #25200F;
    border: 1px solid #B8860B;
    border-radius: 10px;
    color: #FFD95A;
}

/* DIVIDERS */
hr {
    border-color: #6B541A !important;
}

/* CHART CONTAINERS */
div[data-testid="stImage"],
div[data-testid="stPyplot"] {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

movies_df = pd.read_csv(r"CLEANED_DATA\movies.csv")
genres_df = pd.read_csv(r"CLEANED_DATA\genres.csv")
cast_df = pd.read_csv(r"CLEANED_DATA\cast.csv")
movie_genres_df = pd.read_csv(r"CLEANED_DATA\movie_genres.csv")

from sqlalchemy import create_engine
engine = create_engine("mysql+mysqlconnector://root:@localhost/tmdb")

movies_df["release_date"] = pd.to_datetime(
    movies_df["release_date"], errors="coerce"
)
import streamlit as st
from streamlit_option_menu import option_menu


with st.sidebar:
    selected = option_menu(
    "Main Menu",
    ["Home", "Dashboard", "Query", "Visualization"],
    icons=["house", "speedometer2", "database", "bar-chart"],
    menu_icon="cast",
    default_index=0
)
    st.divider()
    st.subheader("🎯 Movie Filters")

    # Genre filter
    genre_list = genres_df["genre_name"].dropna().unique().tolist()

    selected_genres = st.multiselect(
        "Select Genre",
        genre_list,
        key="selected_genres"
    )

    # Release year filter
    min_year = int(movies_df["release_date"].dt.year.min())
    max_year = int(movies_df["release_date"].dt.year.max())

    selected_years = st.slider(
        "Release Year",
        min_year,
        max_year,
        (min_year, max_year),
        key="selected_years"
    )

    # Minimum rating
    min_rating = st.slider(
        "Minimum Rating",
        0.0, 10.0, 0.0, 0.5,
        key="min_rating"
    )

    # Language filter
    language_list = sorted(
        movies_df["original_language"].dropna().unique().tolist()
    )

    selected_language = st.selectbox(
        "Select Language",
        ["All"] + language_list,
        key="selected_language"
    )

movies_df["release_date"] = pd.to_datetime(
    movies_df["release_date"], errors="coerce"
) 

# Apply selected filters
filtered_movies = movies_df.copy()

# Genre filter
if selected_genres:
    genre_data = movie_genres_df.merge(
        genres_df, on="genre_id"
    )

    genre_data = genre_data[
        genre_data["genre_name"].isin(selected_genres)
    ]

    filtered_movies = filtered_movies[
        filtered_movies["movie_id"].isin(genre_data["movie_id"])
    ]

# Release year filter
filtered_movies = filtered_movies[
    filtered_movies["release_date"].dt.year.between(
        selected_years[0], selected_years[1]
    )
]

# Rating filter
filtered_movies = filtered_movies[
    filtered_movies["vote_average"] >= min_rating
]

# Language filter
if selected_language != "All":
    filtered_movies = filtered_movies[
        filtered_movies["original_language"] == selected_language
    ]

# Matching movie count
with st.sidebar:
    st.metric("🎬 Matching Movies", len(filtered_movies))

if selected == "Home":

    # Welcome banner
    st.markdown("""
    <div style="background: linear-gradient(120deg, #24243e, #e50914);
                padding: 40px;
                border-radius: 15px;
                text-align: center;">
        <h1 style="color: white;">🎬 TMDB MOVIE INSIGHTS</h1>
        <p style="color: white; font-size: 18px;">
            Explore the world of cinema through data
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # Project overview
    st.subheader("🎯 Project Overview")

    st.write(
        "Discover movie trends, explore genres, analyze ratings "
        "and understand the movie industry using data analytics."
    )

    st.write("")

    # Database statistics
    st.subheader("📊 Database Statistics")

    col1, col2 = st.columns(2)

    col1.metric("🎬 Total Movies", "2,503")
    col2.metric("🎭 Total Genres", "19")

    st.write("")

    # Dashboard sections
    st.subheader("🚀 Explore Your Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            "🗄️ SQL Query\n\n"
            "Explore movie data using SQL queries."
        )

    with col2:
        st.success(
            "📈 Visualizations\n\n"
            "Discover patterns through interactive charts."
        )

# DASHBOARD PAGE
if selected == "Dashboard":

    st.title("📊 TMDB Movie Dashboard")
    st.write("Explore movie statistics based on your selected filters.")

    # Check filtered data
    if filtered_movies.empty:
        st.warning("No movies match the selected filters.")

    else:
        # KPI calculations
        total_movies = filtered_movies['movie_id'].nunique()

        filtered_genres = movie_genres_df[
            movie_genres_df['movie_id'].isin(filtered_movies['movie_id'])
        ]

        total_genres = filtered_genres['genre_id'].nunique()

        filtered_cast = cast_df[
            cast_df['movie_id'].isin(filtered_movies['movie_id'])
        ]

        total_actors = filtered_cast['actor_name'].nunique()

        average_rating = filtered_movies['vote_average'].mean()

        # KPI Cards
        st.subheader("📌 Key Performance Indicators")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("🎬 Total Movies", total_movies)
        c2.metric("🎭 Total Genres", total_genres)
        c3.metric("👥 Total Actors", total_actors)
        c4.metric("⭐ Average Rating", round(average_rating, 2))

        st.divider()

        # Top 10 movies by revenue
        st.subheader("🏆 Top 10 Movies by Revenue")

        top_movies = filtered_movies.nlargest(10, 'revenue')

        st.bar_chart(
            top_movies,
            x='title',
            y='revenue'
        )

        st.divider()

        # Genre distribution
        st.subheader("🎭 Genre Distribution")

        genre_data = filtered_genres.merge(
            genres_df, on='genre_id'
        )

        genre_counts = genre_data.groupby('genre_name')[
            'movie_id'
        ].nunique().sort_values(ascending=False)

        if not genre_counts.empty:
            st.bar_chart(genre_counts)

        st.divider()

        # Budget vs Revenue
        st.subheader("💰 Budget vs Revenue")

        scatter_data = filtered_movies.dropna(
            subset=['budget', 'revenue']
        )

        st.scatter_chart(
            scatter_data,
            x='budget',
            y='revenue'
        )

        st.divider()

        # Text insight: Highest-grossing genre
        st.subheader("💡 Movie Insights")

        revenue_data = genre_data.merge(
            filtered_movies[['movie_id', 'revenue']],
            on='movie_id'
        )

        genre_revenue = revenue_data.groupby('genre_name')[
            'revenue'
        ].sum().sort_values(ascending=False)

        if not genre_revenue.empty:
            highest_genre = genre_revenue.idxmax()
            highest_revenue = genre_revenue.max()

            st.success(
                f"{highest_genre} is the highest-grossing genre "
                f"in your selected filters, with total revenue "
                f"of ${highest_revenue:,.0f}."
            )

if selected == "Query":
    option = st.selectbox(
    "SELECT A QUERY",
    ("List all movies in the Action genre released after 2015, showing title and release date.", 
     "Find the top 10 highest-grossing movies along with the genre(s) each belongs to.", 
     "Calculate the average budget and average revenue for each genre, sorted by average revenue descending.",
     "List the top 10 actors who have appeared in the most movies in the dataset.(cast)",
     "Find all directors who have directed more than 3 movies, along with their movie count.",
     "List the top 10 most frequently used keywords across all movies.",
     "Find movies where the budget was above the overall average budget but the revenue was below the overall average revenue.",
     "List all actors who have appeared in a movie directed by a specific director (e.g., Christopher Nolan)",
     "Find the genre with the highest average rating, considering only genres with at least 20 movies.",
     "List the top 10 movies with the highest number of keywords tagged to them."),
)
    if option == "List all movies in the Action genre released after 2015, showing title and release date.":
        df = pd.read_sql("SELECT title, release_date FROM movies JOIN movie_genres USING (movie_id) JOIN genres USING (genre_id) WHERE genre_name = 'Action' AND release_date >= '2015-12-31'", con=engine)
        st.dataframe(df)
        df['release_year'] = pd.to_datetime(df['release_date']).dt.year
        st.bar_chart(df['release_year'].value_counts().sort_index())
        st.info(f"Found {len(df)} Action movies released after 2015.")

    elif option == "Find the top 10 highest-grossing movies along with the genre(s) each belongs to.":
        df = pd.read_sql("SELECT title, revenue FROM movies JOIN movie_genres USING (movie_id) JOIN genres USING (genre_id) ORDER BY revenue DESC LIMIT 10", con=engine)
        st.dataframe(df)
        st.bar_chart(df.set_index("title")['revenue'])
        st.info(f"{df.iloc[0]['title']} is the highest-grossing movie with revenue of ${df.iloc[0]['revenue']:,.0f}.")

    elif option == "Calculate the average budget and average revenue for each genre, sorted by average revenue descending.":
        df = pd.read_sql("SELECT genre_name, AVG(revenue),AVG(budget) FROM movies JOIN movie_genres USING (movie_id) JOIN genres USING (genre_id) GROUP BY genre_name ORDER BY AVG(revenue) DESC", con=engine)
        st.dataframe(df)
        st.bar_chart(df.set_index("genre_name")['AVG(revenue)'])
        st.info(f"{df.iloc[0]['genre_name']} has the highest average revenue of ${df.iloc[0]['AVG(revenue)']:,.0f}.")

    elif option == "List the top 10 actors who have appeared in the most movies in the dataset.(cast)":
        df = pd.read_sql("SELECT actor_name, COUNT(movie_id) FROM cast GROUP BY actor_name ORDER BY COUNT(movie_id) DESC LIMIT 10", con=engine)
        st.dataframe(df)
        st.bar_chart(df.set_index("actor_name")['COUNT(movie_id)'])
        st.info(f"{df.iloc[0]['actor_name']} has appeared in the most movies ({df.iloc[0]['COUNT(movie_id)']}).")

    elif option == "Find all directors who have directed more than 3 movies, along with their movie count.":
        df = pd.read_sql(" SELECT person_name, COUNT(movie_id) FROM crew GROUP BY person_name HAVING COUNT(movie_id) > 3 ORDER BY COUNT(movie_id) DESC LIMIT 10", con=engine)
        st.dataframe(df)
        st.bar_chart(df.set_index("person_name")['COUNT(movie_id)'])
        st.info(f"{df.iloc[0]['person_name']} has directed the most movies in this result ({df.iloc[0]['COUNT(movie_id)']}).")
        
    elif option == "List the top 10 most frequently used keywords across all movies.":
        df = pd.read_sql("SELECT keyword_name, COUNT(movie_id) FROM movie_keywords GROUP BY keyword_name ORDER BY COUNT(movie_id) DESC LIMIT 10", con=engine)
        st.dataframe(df)
        st.bar_chart(df.set_index("keyword_name")['COUNT(movie_id)'])
        st.info(f"'{df.iloc[0]['keyword_name']}' is the most frequently used keyword ({df.iloc[0]['COUNT(movie_id)']} movies).")

    elif option == "Find movies where the budget was above the overall average budget but the revenue was below the overall average revenue.": 
        df = pd.read_sql(" SELECT title, budget, revenue FROM movies WHERE budget >(SELECT AVG(budget) FROM movies) AND revenue<(SELECT AVG(revenue) FROM movies)", con=engine)
        st.dataframe(df)
        st.bar_chart(df.set_index("title")['budget'])
        st.info(f"Found {len(df)} movies with above-average budgets but below-average revenues.")

    elif option == "List all actors who have appeared in a movie directed by a specific director (e.g., Christopher Nolan)":
        df = pd.read_sql("SELECT person_name, actor_name FROM cast JOIN crew USING (movie_id) WHERE job = 'director' AND person_name = 'Christopher Nolan'", con=engine)
        st.dataframe(df)
        st.bar_chart(df.set_index("actor_name")['person_name'])
        st.info(f"{df['actor_name'].nunique()} actors are listed in Christopher Nolan's movies.")

    elif option == "Find the genre with the highest average rating, considering only genres with at least 20 movies.":
        df = pd.read_sql("SELECT genre_name, AVG(vote_average) FROM movies JOIN movie_genres USING (movie_id) JOIN genres USING (genre_id) GROUP BY genre_name ORDER BY AVG(vote_average) DESC", con=engine)
        st.dataframe(df)
        st.bar_chart(df.set_index("genre_name")['AVG(vote_average)'])
        st.info(f"{df.iloc[0]['genre_name']} has the highest average rating ({df.iloc[0]['AVG(vote_average)']:.2f}/10).")

    elif option == "List the top 10 movies with the highest number of keywords tagged to them.":
        df = pd.read_sql("SELECT title, count(keyword_id) FROM movies JOIN movie_keywords USING(movie_id) GROUP BY title ORDER BY count(keyword_id) DESC LIMIT 10", con=engine)
        st.dataframe(df)
        st.bar_chart(df, x="title", y="count(keyword_id)")
        st.info(f"{df.iloc[0]['title']} has the most keywords ({df.iloc[0]['count(keyword_id)']}).")

if selected == "Visualization":
    c1,c2,c3 = st.columns([0.45,0.1,0.45   ])
    with c1:
        st.subheader("Correlation Heatmap ",divider = 'rainbow')
        num_cols = filtered_movies.select_dtypes(include="number").columns.drop("movie_id")

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(filtered_movies[num_cols].corr(), annot=True, fmt=".2f", cmap="coolwarm")
        st.pyplot(fig)
    with c3:
        st.subheader("Movies per Year", divider='rainbow')
        movies_per_year = filtered_movies.groupby(
            filtered_movies["release_date"].dt.year
        ).size()

        fig, ax = plt.subplots()
        ax.plot(movies_per_year.index, movies_per_year.values)

        ax.set_xlabel("Year")
        ax.set_ylabel("Number of Movies")
        st.pyplot(fig)

    
if selected == "Visualization":

    st.title("📊 Movie Data Visualizations")
    st.write("Explore all  visualizations ")

    viz_movies = filtered_movies.copy()

    # Remove invalid values for charts where needed
    viz_movies["release_year"] = viz_movies["release_date"].dt.year
    viz_movies["release_decade"] = (viz_movies["release_year"] // 10) * 10

    # Prepare genre data
    genre_data = movie_genres_df[
        movie_genres_df["movie_id"].isin(viz_movies["movie_id"])
    ].merge(genres_df, on="genre_id")

    # 1. Budget Distribution
    st.subheader("1. Budget Distribution")
    fig, ax = plt.subplots()
    sns.histplot(viz_movies[viz_movies["budget"] > 0]["budget"], kde=True, ax=ax)
    ax.set_xlabel("Budget")
    st.pyplot(fig)
    plt.close(fig)

    # 2. Runtime Box Plot
    st.subheader("2. Runtime Distribution")
    fig, ax = plt.subplots()
    sns.boxplot(y=viz_movies[viz_movies["runtime"] > 0]["runtime"], ax=ax)
    ax.set_ylabel("Runtime (Minutes)")
    st.pyplot(fig)
    plt.close(fig)

    # 3. Vote Average Distribution
    st.subheader("3. Vote Average Distribution")
    fig, ax = plt.subplots()
    sns.histplot(viz_movies["vote_average"].dropna(), bins=20, kde=True, ax=ax)
    ax.set_xlabel("Vote Average")
    st.pyplot(fig)
    plt.close(fig)

    # 4. Movies per Genre
    st.subheader("4. Number of Movies per Genre")
    genre_counts = genre_data.groupby("genre_name")["movie_id"].nunique().sort_values()
    fig, ax = plt.subplots()
    genre_counts.plot(kind="bar", ax=ax)
    ax.set_ylabel("Number of Movies")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)
    plt.close(fig)

    # 5. Budget vs Revenue
    st.subheader("5. Budget vs Revenue")
    data = viz_movies[(viz_movies["budget"] > 0) & (viz_movies["revenue"] > 0)]
    fig, ax = plt.subplots()
    sns.regplot(data=data, x="budget", y="revenue", scatter_kws={"alpha": 0.5}, ax=ax)
    st.pyplot(fig)
    plt.close(fig)

    # 6. Popularity vs Vote Count
    st.subheader("6. Popularity vs Vote Count")
    fig, ax = plt.subplots()
    sns.scatterplot(data=viz_movies, x="vote_count", y="popularity", ax=ax)
    st.pyplot(fig)
    plt.close(fig)

    # 7. Average Rating by Genre
    st.subheader("7. Average Rating by Genre")
    rating_data = genre_data.merge(
        viz_movies[["movie_id", "vote_average"]], on="movie_id"
    )
    avg_rating = rating_data.groupby("genre_name")["vote_average"].mean().sort_values()
    fig, ax = plt.subplots()
    avg_rating.plot(kind="bar", ax=ax)
    ax.set_ylabel("Average Rating")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)
    plt.close(fig)

    # 8. Movies Released per Year
    st.subheader("8. Movies Released per Year")
    yearly_movies = viz_movies.groupby("release_year")["movie_id"].nunique()
    fig, ax = plt.subplots()
    yearly_movies.plot(kind="line", marker="o", ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Movies")
    st.pyplot(fig)
    plt.close(fig)

    # 9. Correlation Heatmap
    st.subheader("9. Correlation Heatmap")
    num_cols = viz_movies.select_dtypes(include="number").columns.drop(
        "movie_id", errors="ignore"
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(viz_movies[num_cols].corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    st.pyplot(fig)
    plt.close(fig)

    # 10. Pair Plot
    st.subheader("10. Pair Plot")
    pair_cols = ["budget", "revenue", "popularity", "vote_average"]
    pair_data = viz_movies[pair_cols].dropna()
    pair_data = pair_data.sample(min(500, len(pair_data)), random_state=42)

    if len(pair_data) > 1:
        pair_fig = sns.pairplot(pair_data)
        st.pyplot(pair_fig.fig)
        plt.close(pair_fig.fig)

    # 11. Budget vs Revenue by Primary Genre
    st.subheader("11. Budget vs Revenue by Primary Genre")

    primary_genre = genre_data.drop_duplicates("movie_id")
    primary_data = viz_movies.merge(
        primary_genre[["movie_id", "genre_name"]], on="movie_id"
    )
    primary_data = primary_data[
        (primary_data["budget"] > 0) & (primary_data["revenue"] > 0)
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=primary_data, x="budget", y="revenue",
        hue="genre_name", ax=ax
    )
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    st.pyplot(fig)
    plt.close(fig)

    # 12. Vote Average by Genre
    st.subheader("12. Vote Average Distribution by Genre")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=rating_data, x="genre_name", y="vote_average", ax=ax)
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)
    plt.close(fig)

    # 13. Average Revenue by Genre and Decade
    st.subheader("13. Average Revenue by Genre and Decade")

    decade_data = genre_data.merge(
        viz_movies[["movie_id", "revenue", "release_decade"]],
        on="movie_id"
    )

    decade_data = decade_data[decade_data["revenue"] > 0]

    revenue_pivot = decade_data.pivot_table(
        index="genre_name",
        columns="release_decade",
        values="revenue",
        aggfunc="mean"
    )

    fig, ax = plt.subplots(figsize=(12, 7))
    sns.heatmap(revenue_pivot, annot=True, fmt=".0f", cmap="YlOrRd", ax=ax)
    ax.set_xlabel("Release Decade")
    ax.set_ylabel("Genre")
    st.pyplot(fig)
    plt.close(fig)
