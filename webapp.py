import streamlit as st
import pickle
import requests

movies = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

movies_list = movies['title'].values
st.header("Movie Recommendation System")

select_value = st.selectbox("Select Movie Please from the Dropdown", movies_list)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
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

if st.button("Show Recommend"):
    movie_name, movie_poster = recommand(select_value)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])  # Make sure this is 'st.image'
        
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])  # Make sure this is 'st.image'
        
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])  # Make sure this is 'st.image'
        
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])  # Make sure this is 'st.image'
        
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])  # Make sure this is 'st.image'
