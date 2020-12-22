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
    fig.update_layout(autosize=True, height=300, margin=dict(b=10, t=10))
    return fig


def sentiment_overview(df):
    st.subheader('Overview of comments')
    st.write('Sort the comments by sentiment based on polarity and then it displays them in the list below.')
    option = st.selectbox(
        'Select the sentiment',
        ('Positive', 'Negative', 'Neutral'))

    if option == 'All':
        if len(df['comments'].tolist()) > 0:
            st.table(df['comments'])
        else:
            st.info('There is no comments on this video.')
    else:
        if len(df[df['sentiment'] == lowerstrip(option)]['comments'].tolist()) > 0:
            st.table(df[df['sentiment'] == lowerstrip(option)]
                     ['comments'])
        else:
            st.info(
                f'There is no {lowerstrip(option)} comments on this video.')


def streamlit_config():
    st.set_page_config(
        page_title='YTOM')
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


if __name__ == "__main__":
    streamlit_config()
    DEVELOPER_KEY = os.environ.get('YOUTUBE_SECRET_KEY', None)
    youtube = get_authenticated_service(DEVELOPER_KEY)
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
        if int(video_snippet['statistics']['commentCount']) > 5000:
            st.error('Video exceed the limit of 5000 comments.')
            st.header('Video exceed the limit of comments.')
            st.write(
                'For performance and cost reasons, this service is limited to videos with less than 5000 comments. If you are interested in more, please contact me.')
            st.write('https://www.linkedin.com/in/loic-rouiller-monay/')
        else:
            st.info(
                f'{ video_snippet["snippet"]["channelTitle"] } ~ { video_snippet["snippet"]["title"] }')
            with st.spinner('Processing...'):
                comments = get_comment_threads(
                    youtube, video_id, comments=[], token="")
                df = sentiment_analysis(comments)
                df_value_counts = sentiment_analysis_value_counts(df)

            st.subheader('Sentiment analysis')
            st.write(
                'The table and figure below shows the distribution of sentiments in the video comments.')
            st.table(df_value_counts)

            fig = get_fig(df_value_counts)
            st.plotly_chart(fig, use_container_width=True)

            sentiment_overview(df)
