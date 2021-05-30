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


type_text = st.selectbox("Type of Text", ['POSTS', 'COMMENTS'])

db = Database()
db.use_database('DB1')


if type_text=='POSTS':
	ids = db.query("SELECT POST_ID FROM POSTS WHERE TARGET=-1 ;")

else:
	ids = db.query("SELECT COMMENT_ID FROM COMMENTS WHERE TARGET=-1 ;")
count = 0	



placeholder = st.empty()
start = placeholder.button("Start")

if start:
	placeholder.empty()
	stop = placeholder.button("Stop")
	placeholder2 = st.empty()
	display_text = st.empty()
	positive = st.empty()
	negative = st.empty()
	con = st.empty()
	#= col1, col2 = st.beta_columns([.5,1])
	
	while (not stop) and (count<=len(ids)):

		positive.button("Positive", key='1')
		negative.button("Negative", key='0')
		placeholder2.text("Running")
		con.button("Continue")
		

		if type_text=='POSTS':

		
			display_text.text(db.query("SELECT TITLE FROM POSTS WHERE POST_ID='{}'".format(ids[0][0])))
			if positive and con:
				st.text("POSITIVE")
				count+=1
			if negative:
				st.text("NEGATIVE")
				count+=1




		else:
			
			display_text.text(db.query("SELECT COMMENT FROM COMMENTS WHERE COMMENT_ID='{}'".format(i[0][0])))
			if positive and con:
				st.text("POSITIVE")
				count+=1
			if negative:
				st.text("NEGATIVE")
				count+=1


		


		#db.label(type_text,)








