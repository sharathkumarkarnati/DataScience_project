import streamlit as st
import pickle
import requests

# Load movie data
movies = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# Setting page configuration
st.set_page_config(page_title="🎬 Movie Recommendation System", layout="wide")

# Add custom CSS for styling
st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
        }
        .header {
            font-size: 36px; 
            color: #e74c3c;
            text-align: center;
        }
        .recommendations img {
            border-radius: 10px;
            transition: transform 0.3s;
        }
        .recommendations img:hover {
            transform: scale(1.05);
        }
        .sidebar-text {
            font-size: 18px; 
            color: #2c3e50;
            margin: 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

# TMDB API configurations
API_KEY = "c7ec19ffdd3279641fb606d19ceb9bb1"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500/"

# Header
st.markdown("<h1 class='header'>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)

movies_list = movies['title'].values
tab1, tab2, tab3 = st.tabs(["Recommendations", "Top Rated Movies", "Favorites"])

# Helper function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    return TMDB_IMAGE_BASE_URL + data.get("poster_path", "")

# Helper function to fetch top-rated movies
def fetch_top_rated_movies():
    url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}&language=en-US&page=1"
    data = requests.get(url).json()
    return data["results"][:5]  # Fetch top 5 movies

# Helper function to recommend movies
def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# Recommendations Tab
with tab1:
    select_value = st.selectbox("Select a Movie to Get Recommendations", movies_list)
    if st.button("Show Recommendations", key="recommend_btn"):
        movie_names, movie_posters = recommend(select_value)
        cols = st.columns(5)
        for col, name, poster in zip(cols, movie_names, movie_posters):
            with col:
                st.image(poster, use_column_width=True, caption=name)

# Top Rated Movies Tab
with tab2:
    st.subheader("🔥 Top Rated Movies")
    top_movies = fetch_top_rated_movies()
    cols = st.columns(5)
    for col, movie in zip(cols, top_movies):
        poster_url = TMDB_IMAGE_BASE_URL + movie["poster_path"]
        with col:
            st.image(poster_url, use_column_width=True, caption=movie["title"])

# Sidebar for Favorites
# Initialize session state
if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

# Add to favorites button
if st.button("Add to Favorites", key="add_to_favorites"):
    if select_value not in st.session_state["favorites"]:
        st.session_state["favorites"].append(select_value)
        st.success(f"Added '{select_value}' to favorites!")
    else:
        st.warning(f"'{select_value}' is already in your favorites.")

# Show favorite movies in sidebar
if st.sidebar.button("Show Favorites"):
    if st.session_state["favorites"]:
        st.sidebar.header("Your Favorite Movies")
        for favorite in st.session_state["favorites"]:
            st.sidebar.text(favorite)
    else:
        st.sidebar.text("No favorites added yet.")


# Favorites Tab
with tab3:
    if st.button("Add to Favorites", key="add_favorites"):
        if select_value not in st.session_state.favorites:
            st.session_state.favorites.append(select_value)
            st.success(f"Added '{select_value}' to your favorites!")
        else:
            st.warning(f"'{select_value}' is already in your favorites.")
    st.subheader("Your Favorite Movies")
    if st.session_state.favorites:
        for favorite in st.session_state.favorites:
            st.write(f"- {favorite}")
    else:
        st.write("You haven't added any favorite movies yet.")

# Sidebar for managing favorites
st.sidebar.header("Manage Favorites")
if st.sidebar.button("Clear Favorites"):
    st.session_state.favorites = []
    st.sidebar.success("Favorites cleared!")

# Footer
st.markdown("<p style='text-align: center; color: gray;'>Made with ❤️ using Streamlit @ Sharath Karnati</p>", unsafe_allow_html=True)
