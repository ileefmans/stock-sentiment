import streamlit as st
from inference import pull, RunInference







class App:
	"""
		Class for primary application
	"""
	def __init__(self):
		st.title('**Stock Sentiment**')
		st.markdown(""" #### Application for scraping redit for metrics and visualizations regarding sentiment towards a particular stock """)
		#st.text("IMPORTANT: You must set sentiment to 'select sentiment' when choosing 'POSTS' or 'COMMENTS'")
		st.text("")
		st.text("")
		st.text("")


		self.stock_id = st.sidebar.text_input("Stock Symbol")
		self.mode = st.sidebar.selectbox("Mode", ['*Choose Mode*','Visualization', 'Prediction'], index=0)
		self.go = st.sidebar.button("Go")







if __name__ == '__main__':
	app = App()



