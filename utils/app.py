import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
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
           

    def density_plot(self, data, title, xlabel):
        plt.style.use('dark_background')
        ser = pd.Series(data[:,1])

        fig, ax = plt.subplots(figsize=(10,6))

        sns.kdeplot(ser, color="red", shade=True)

        ax.set_title(title, fontdict = {'fontsize': 20}, pad = 15)
        ax.set_xlabel(xlabel, fontsize=14, labelpad = 20)
        ax.set_ylabel('Density', fontsize=14, labelpad=20)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        return fig



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

            with st.spinner("Running inference..."):
                run_inference = RunInference(stock_id=self.stock_id)
                inference_output = run_inference.evaluate()
            if not inference_output:
                st.text("Not enough recent posts")
            else:

                post_probs = inference_output['avg_post_probs']
                comment_probs = inference_output['avg_comment_probs']
                all_post_probs = inference_output['all_post_probs']
                all_comment_probs = inference_output['all_comment_probs']


                st.pyplot(self.density_plot(
                    data=all_post_probs, 
                    title="Density Plot of Post Probabilities", 
                    xlabel='Probability of Positive Sentiment'
                    )
                )

                st.pyplot(self.density_plot(
                    data = all_comment_probs,
                    title = "Density Plot of Comment Probabilities",
                    xlabel = 'Probability of Positive Sentiment'
                    )
                )








if __name__ == '__main__':
    app = App()
    app.run()





