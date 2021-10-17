import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import streamlit as st
from inference import pull, RunInference
from forecast import Forecast








class App:
    """
        Class for primary application
    """
    def __init__(self, testing_env=False):
        st.title('**Stock Sentiment**')
        st.markdown(""" #### Application for scraping Reddit for metrics, visualizations, and predictions regarding sentiment towards a particular stock """)
        st.text("")
        st.text("")
        st.text("")

        self.testing_env = testing_env
        self.stock_id = st.sidebar.text_input("Stock Symbol")
        #self.mode = st.sidebar.selectbox("Mode", ['*choose mode','Visualization', 'Prediction'], index=0)
        self.go = st.sidebar.button("Go")
        


    def density_plot(self, data, title, xlabel):
        plt.style.use('dark_background')
        ser = pd.Series(data[:,1])

        fig, ax = plt.subplots(figsize=(10,6))

        sns.kdeplot(ser, color="red", shade=True)

        ax.set_title(title, fontdict = {'fontsize': 20}, pad = 15)
        ax.set_xlabel(xlabel, fontsize=14, labelpad = 20)
        ax.set_ylabel('Density', fontsize=14, labelpad=20)
        ax.set_xlim(left=0, right=1)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        return fig


    def prediction_plot(self, data):
        plt.style.use('dark_background')

        fig, ax = plt.subplots(figsize=(10,6))



        data.loc[data.is_pred==0,:].plot.line(ax=ax, x="timestamp", y="close_price", color='darkred')
        data.loc[data.is_pred==1,:].plot.line(ax=ax, x="timestamp", y="close_price", color='lightsteelblue')

        ax.set_title("Predictions", fontdict = {'fontsize': 20}, pad = 15)
        ax.set_xlabel('date', fontsize=14, labelpad = 20)
        ax.set_ylabel('close price', fontsize=14, labelpad=20)

        ax.legend(['price', 'predicted price'])
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        return fig


    @st.cache(suppress_st_warning=True)
    def infer(self):
        with st.spinner("Checking to see if database needs to be updated..."):
            if self.testing_env:
                pull(
                    value=48,
                    stock_id=self.stock_id,
                    num_posts=5,
                    num_comments=1,
                    increment='HOUR'
                    )
            else:
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
        return inference_output

    def run(self):
        if self.go:


            inference_output = self.infer()

            with st.spinner("Forecasting..."):
                forecast = Forecast(self.stock_id, inference_output)
                stock_preds = forecast.arima()
                
            
                
            if not inference_output:
                st.text("Not enough recent posts")
            else:

                post_probs = inference_output['avg_post_probs']
                comment_probs = inference_output['avg_comment_probs']
                all_post_probs = inference_output['all_post_probs']
                all_comment_probs = inference_output['all_comment_probs']

                my_expander1 = st.beta_expander("Positive Examples")
                with my_expander1:
                    st.text("")
                    cola, colb = st.beta_columns(2)
                    cola.markdown("#### Most Positive Post: \n\n{}".format(inference_output['max_post']))
                    cola.markdown(f"#### Predicted Probability of Being positive: \n\n{round(inference_output['max_post_prob'], 4)}")

                    colb.markdown("#### Most Positive Comment: \n\n{}".format(inference_output['max_comment']))
                    colb.markdown(f"#### Predicted Probability of Being positive: \n\n{round(inference_output['max_comment_prob'], 4)}")


                my_expander2 = st.beta_expander("Negative Examples")
                with my_expander2:
                    st.text("")
                    # example = st.multiselect("Display Example", ['Post', 'Comment'])
                    st.text("")
                    colc, cold = st.beta_columns(2)
                    # if 'Post' in example:
                    colc.markdown("#### Most Negative Post: \n\n{}".format(inference_output['min_post']))
                    colc.markdown(f"#### Predicted Probability of Being Positive: \n\n{round(inference_output['min_post_prob'], 4)}")
                    # if 'Comment' in example:
                    cold.markdown("#### Most Negative Comment: \n\n{}".format(inference_output['min_comment']))
                    cold.markdown(f"#### Predicted Probability of Being Positive: \n\n{round(inference_output['min_comment_prob'], 4)}")



                my_expander3 = st.beta_expander("Density Plot of Sentiment")
                with my_expander3:
                    st.text("")


                    col1, col2 = st.beta_columns(2)

                    col1.pyplot(self.density_plot(
                        data=all_post_probs, 
                        title="Density Plot of Post Probabilities", 
                        xlabel='Probability of Positive Sentiment'
                        )
                    )

                    col2.pyplot(self.density_plot(
                        data = all_comment_probs,
                        title = "Density Plot of Comment Probabilities",
                        xlabel = 'Probability of Positive Sentiment'
                        )
                    )
                    print('\n \n \n')
                    print(all_post_probs)
                    print('\n \n ')
                    print(all_comment_probs)


                my_expander4 = st.beta_expander("Stock Forecast")
                with my_expander4:
                    st.text("")

                    st.pyplot(self.prediction_plot(
                        data = stock_preds
                        )
                    )

                    







if __name__ == '__main__':
    app = App(testing_env=True)
    app.run()





