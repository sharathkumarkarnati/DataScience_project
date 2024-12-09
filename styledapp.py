import streamlit as st
import pickle
import requests

# Load movie data
movies = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# Setting page configuration
st.set_page_config(page_title="Movie Recommendation System", layout="wide")

# Adding custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #f4f4f4;  /* Light background for the whole app */
            color: #2c3e50;  /* Dark text color */
        }
        .header {
            font-size: 36px; 
            color: #e74c3c;  /* Red header */
            text-align: center; 
            margin-bottom: 20px;
        }
        .subheader {
            font-size: 24px; 
            color: #3498db;  /* Blue for subtitles */
        }
        .main {
            padding: 20px; 
            border-radius: 10px; 
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            background-color: rgba(255, 255, 255, 0.9);  /* White background for main area */
        }
        img {
            border-radius: 10px;
            transition: transform 0.2s; 
            width: 250px;  /* Size of the posters */
        }
        img:hover {
            transform: scale(1.1);
        }
        .button {
            background-color: #27ae60;  /* Green buttons */
            color: white; 
            border: None; 
            border-radius: 5px; 
            padding: 10px 20px; 
            cursor: pointer;
            transition: background-color 0.3s, transform 0.3s;
            display: inline-block;  
            text-align: center;
            margin: 10px;  /* Spacing between buttons */
        }
        .button:hover {
            background-color: #219653;  /* Darker green on hover */
            transform: scale(1.05);
        }
        .fav-btn {
            background-color: #2980b9;  /* Bright blue for favorites */
            padding: 10px 20px;
            margin: 10px;  /* Spacing between buttons */
        }
        .fav-btn:hover {
            background-color: #1f6393;  /* Darker blue on hover */
        }
    </style>
""", unsafe_allow_html=True)

# Display movie titles
st.header("🎬 Movie Recommendation System")
select_value = st.selectbox("Select a Movie from the Dropdown", movies['title'].values)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

def recommand(movie):
    index = movies[movies["title"] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    
    recommand_movies = []
    recommand_poster = []
    
    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommand_movies.append(movies.iloc[i[0]].title)
        recommand_poster.append(fetch_poster(movie_id))
        
    return recommand_movies, recommand_poster

# Button for showing recommendations
if st.button("Show Recommendations", key="show_recommendations"):
    movie_name, movie_poster = recommand(select_value)
    
    cols = st.columns(5)
    
    for col, name, poster in zip(cols, movie_name, movie_poster):
        with col:
            st.image(poster)
            st.text(name)

# Favorite Movies Feature
if "favorites" not in st.session_state:
    st.session_state.favorites = []

if st.button("Add to Favorites", key="add_to_favorites"):
    if select_value not in st.session_state.favorites:
        st.session_state.favorites.append(select_value)
        st.success(f"Added '{select_value}' to favorites!")
    else:
        st.warning(f"'{select_value}' is already in your favorites.")

# Show favorite movies
if st.sidebar.button("Show Favorites"):
    if st.session_state.favorites:
        st.sidebar.header("Your Favorite Movies")
        for favorite in st.session_state.favorites:
            st.sidebar.text(favorite)
    else:
        st.sidebar.text("No favorites added yet.")
