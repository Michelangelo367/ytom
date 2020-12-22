import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from textblob.utils import lowerstrip
from src.ytom import *


def get_fig_colors(df):
    colors = []
    for sentiment in df['sentiment']:
        if sentiment == 'positive':
            colors.append('green')
        if sentiment == 'negative':
            colors.append('crimson')
        if sentiment == 'neutral':
            colors.append('black')
    return colors


def get_fig(df):
    colors = get_fig_colors(df)
    fig = go.Figure(data=[go.Bar(
        x=df['sentiment'],
        y=df['count'],
        text=df['count'],
        textposition='auto',
        marker_color=colors
    )])
    fig.update_layout(autosize=False,
                      width=500, height=300,
                      margin=dict(l=180, r=0, b=10, t=10))
    return fig


def sentiment_overview(df):
    st.subheader('Overview of comments')
    option = st.selectbox(
        'Sort the comments by sentiment based on polarity and then it displays them in the list below.',
        ('Positive', 'Negative', 'Neutral'))

    if option == 'All':
        if len(df['text'].tolist()) > 0:
            st.table(df['text'])
        else:
            st.info('There is no comments on the video.')
    else:
        if len(df[df['sentiment'] == lowerstrip(option)]['text'].tolist()) > 0:
            st.table(df[df['sentiment'] == lowerstrip(option)]
                     ['text'])
        else:
            st.info(f'There is no {lowerstrip(option)} comments on the video.')


if __name__ == "__main__":
    youtube = get_authenticated_service()
    st.title('YTOM ~ YouTube Opinion Mining')
    st.subheader('Description')
    st.write(
        'Automatically understand the feelings and emotions from YouTube comments.')

    video_url = st.text_input(
        'Youtube Video URL', 'https://www.youtube.com/watch?v=ASKPfSQvdnM')

    if is_youtube_url(video_url) != True:
        st.error('Invalid YouTube URL')
        st.warning(
            'This URL does not seem to be valid. Please provide a YouTube Video URL in the input field.')
    else:
        video_id = get_video_id_from_youtube_url(video_url)
        video_snippet = get_video_snippet(youtube, video_id)
        st.info(
            f'{ video_snippet["channelTitle"] } ~ { video_snippet["title"] }')
        with st.spinner('Processing...'):
            comments = get_comment_threads(
                youtube, video_id, comments=[], token="")
            df = sentiment_analysis(comments)
            df_value_counts = sentiment_analysis_value_counts(df)

        st.subheader('Sentiment analysis')
        st.table(df_value_counts)

        fig = get_fig(df_value_counts)
        st.plotly_chart(fig)

        sentiment_overview(df)
