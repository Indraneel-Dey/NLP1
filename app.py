import requests
import streamlit as st


def query(url, headers, payload): return requests.post(url, headers=headers, json=payload).json()


def summarize(text):
    url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": "Bearer API KEY"}
    return query(url, headers, {"inputs": str(text), })[0]['summary_text']


def sentiment(text):
    url = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"
    headers = {"Authorization": "Bearer API KEY"}
    output = query(url, headers, {"inputs": str(text), })
    li = [output[0][0]['score'], output[0][1]['score'], output[0][2]['score']]
    if max(li) == li[0]:
        return 'Negative'
    elif max(li) == li[1]:
        return 'Neutral'
    else:
        return 'Positive'


def genre(text, labels):
    url = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
    headers = {"Authorization": "Bearer API KEY"}
    out = query(url, headers, {"inputs": str(text), "parameters": {"candidate_labels": labels}, })
    return out['labels'][out['scores'].index(max(out['scores']))]


st.write('Indraneel Dey')
st.write('Indian Institute of Technology, Madras')
st.title('Text Analysis')

st.write('If you want to summarize a passage:')
passage = str(st.text_area('Enter the passage you want to summarize'))
if st.button('Summarize'):
    st.write(summarize(passage))

st.write('If you want to analyze the sentiment of a piece of text:')
line = str(st.text_area('Enter the statement you want to find the sentiment of'))
if st.button('Analyze'):
    st.write(sentiment(line))

st.write('If you want to find the genre of a passage:')
article = str(st.text_area('Enter the passage you want to find the genre of'))
st.write('Enter up to 5 options for the genre of the passage')
options = [str(st.text_input('Enter the option', '', key=i)) for i in range(5)]
if st.button('Find'):
    st.write(genre(article, options))
