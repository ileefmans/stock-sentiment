from data import Database, ScrapeWSB
import streamlit as st


st.title('**Labeling Interface**')
st.markdown(""" #### Interface to assist in hand labeling posts and comments """)
st.text("IMPORTANT: You must set sentiment to 'select sentiment' when choosing 'POSTS' or 'COMMENTS'")
st.text("")
st.text("")
st.text("")

stock_id = st.sidebar.text_input("Stock Symbol")

num_posts = st.sidebar.slider("Number of Posts", min_value=1, max_value=100)

num_comments = st.sidebar.slider("Number of Comments", min_value=1, max_value=100)


time_filter = st.sidebar.selectbox("Time Filter", ['day', 'week', 'month'], index=0)

scrape = st.sidebar.button("Scrape")

if scrape and stock_id:
	with st.spinner('Scraping...'):
		scrapewsb = ScrapeWSB(stock_id, num_posts, num_comments, time_filter=time_filter)
		df = scrapewsb.scrape()
		scrapewsb.convert(df)





type_text = st.selectbox("Type of Text", ['POSTS', 'COMMENTS'])

db = Database()
db.use_database('DB1')




st.text("")
st.markdown("""#### Text to label:""")
st.text("")

display_text = st.empty() 

st.text("")
st.text("")
sentiment = st.selectbox("Sentiment", ['select sentiment', 'positive', 'negative'], index=0)

display_text_key = '0'






	
	

if type_text == 'POSTS':
	ids = db.query("SELECT POST_ID FROM POSTS WHERE TARGET=-1 ;")
	if len(ids)==0:
		display_text.text("NO UNLABELED {}".format(type_text))
		display_text_key = str(int(display_text_key)+1)
	else:
		if sentiment=="select sentiment":
			display_text.text(db.query("SELECT TITLE FROM POSTS WHERE POST_ID='{}'".format(ids[0][0]))[0][0])
			display_text_key = str(int(display_text_key)+1)
		else:
			display_text.text(db.query("SELECT TITLE FROM POSTS WHERE POST_ID='{}'".format(ids[1][0]))[0][0])
			display_text_key = str(int(display_text_key)+1)
		if (sentiment=='positive'):
			
			
			db.label(type_text, ids[0][0], 1)
			
		if (sentiment=='negative'):
			
			
			db.label(type_text, ids[0][0], 0)

	
		
elif type_text == 'COMMENTS':
	ids = db.query("SELECT COMMENT_ID FROM COMMENTS WHERE TARGET=-1 ;")
	if len(ids)==0:
		display_text.text("NO UNLABELED {}".format(type_text))
		display_text_key = str(int(display_text_key)+1)
	else:
		if sentiment=='select sentiment':
			display_text.text(db.query("SELECT COMMENT FROM COMMENTS WHERE COMMENT_ID='{}'".format(ids[0][0]))[0][0])
			display_text_key = str(int(display_text_key)+1)
		else:
			display_text.text(db.query("SELECT COMMENT FROM COMMENTS WHERE COMMENT_ID='{}'".format(ids[1][0]))[0][0])
			display_text_key = str(int(display_text_key)+1)
		if (sentiment=='positive'):
			
			
			db.label(type_text, ids[0][0], 1)
			
		if (sentiment=='negative'):
			
			
			db.label(type_text, ids[0][0], 0)

	
else:
	display_text.text("NO UNLABELED {}".format(type_text))
	display_text_key = str(int(display_text_key)+1)


