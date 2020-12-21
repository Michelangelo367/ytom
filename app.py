import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.ytom import *


@st.cache
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


@st.cache
def get_fig(df):
    colors = get_fig_colors(df)
    fig = go.Figure(data=[go.Bar(
        x=df['sentiment'],
        y=df['count'],
        textposition='auto',
        marker_color=colors
    )])
    return fig


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
        with st.spinner('Processing...'):
            comments = []
            comments = comments.clear()
            comments = get_comment_threads(
                youtube, video_id, comments=[], token="")
            st.info(len(comments))
            st.write(comments)
            df = sentiment_analysis(comments)

        df

        fig = get_fig(df)
        st.plotly_chart(fig)
