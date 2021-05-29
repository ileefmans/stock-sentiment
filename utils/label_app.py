from data import Database, ScrapeWSB
import streamlit as st


st.title('**Labeling Interface**')
st.markdown(""" #### Interface to assist in hand labeling posts and comments """)
st.text("")
st.text("")

stock_id = st.sidebar.text_input("Stock Symbol")

num_posts = st.sidebar.slider("Number of Posts", min_value=1, max_value=100)

num_comments = st.sidebar.slider("Number of Comments", min_value=1, max_value=100)


time_filter = st.sidebar.selectbox("Time Filter", ['day', 'week', 'month'], index=0)