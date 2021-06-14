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
        self.mode = st.sidebar.selectbox("Mode", ['*choose mode','Visualization', 'Prediction'], index=0)
        self.go = st.sidebar.button("Go")
           


    def run(self):
        if self.go:
            with st.spinner("Checking to see if database needs to be updated..."):
                pull(
                    value=48, 
                    stock_id=self.stock_id, 
                    num_posts=10, 
                    num_comments=5, 
                    increment='HOUR'
                )

            with st.stpinner("Running inference..."):
                run_inference = RunInference(stock_id=self.stock_id)
                inference_output = run_inference.evaluate()

                post_probs = inference_output['avg_post_probs']

                comment_probs = inference_output['avg_comment_probs']

                






if __name__ == '__main__':
    app = App()
    app.run()





