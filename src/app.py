import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from ytom import *

st.title('YTOM ~ YouTube Opinion Mining')
st.subheader('Description')
st.write('Automatically understand the feelings and emotions from YouTube comments.')

video_url = st.text_input(
    'Youtube Video URL', 'https://www.youtube.com/watch?v=ASKPfSQvdnM')

video_id = video_url.split('watch?v=')[1]

# df = pd.DataFrame(
#     data=[[331, 'positive'], [227, 'negative'], [45, 'neutral']],
#     columns=['count', 'sentiment']
# )

# sentiment analysis
comments = get_comments(video_id)
df = sentiment_analysis(comments)

st.subheader('Sentiment analysis')
st.write('The sentiment analysis detects positive, negative or neutral sentiment in the video comments.')

df

colors = []
for sentiment in df['sentiment']:
    if sentiment == 'positive':
        colors.append('green')
    if sentiment == 'negative':
        colors.append('crimson')
    if sentiment == 'neutral':
        colors.append('black')

fig = go.Figure(data=[go.Bar(
    x=df['sentiment'],
    y=df['count'],
    textposition='auto',
    marker_color=colors
)])
st.plotly_chart(fig)
