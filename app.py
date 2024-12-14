import pandas as pd
import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data=response.json()

    return "http://image.tmdb.org/t/p/w500/"+data['poster_path']

movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))




def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]


    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommend_movies=[]
    recommended_movies_poster=[]
    for i in movies_list:
        recommend_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movies.iloc[i[0]].id))

    return recommend_movies,recommended_movies_poster


st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    movies['title'].values,
)
if st.button("Recommend"):
    names , posters=recommend(selected_movie_name)

    col1,col2,col3,col4,col5=st.columns(5)

    with col1:
        st.header(names[0])
        st.image(posters[0])

    with col2:
        st.header(names[1])
        st.image(posters[1])

    with col3:
        st.header(names[2])
        st.image(posters[2])

    with col4:
        st.header(names[3])
        st.image(posters[3])

    with col5:
        st.header(names[4])
        st.image(posters[4])



