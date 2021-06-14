FROM python:3.7

COPY utils/ /utils/
COPY config.yml /
COPY IDs.yml /
COPY requirements.txt /

RUN apt-get update
RUN pip install -r requirements.txt

CMD streamlit run utils/app.py
