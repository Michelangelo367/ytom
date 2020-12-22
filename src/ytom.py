import os
import googleapiclient.discovery
import pandas as pd
from textblob import TextBlob
import re
import logging
import requests
import streamlit as st


def is_youtube_url(url):
    # returns True if the Youtube URL is valid
    regex_youtube_url_validator = (
        r'^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$')
    if re.fullmatch(regex_youtube_url_validator, url):
        try:
            code = requests.get(url).status_code
            if code == 200:
                return True
            else:
                return False
        except Exception as e:
            logging.exception(
                "Error occured while validating YouTube URL.\n", e)
            return False
    else:
        return False


def get_video_id_from_youtube_url(url):
    # get Video ID from YouTube URL
    regex_video_id = (
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')
    match = re.match(regex_video_id, url)
    if match:
        return match.group('id')
    else:
        logging.exception("No video ID found in the URL")
        return ''


def get_authenticated_service():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"
    api_service_name = "youtube"
    api_version = "v3"
    with open("src/.secret/config.txt", "r") as f:
        DEVELOPER_KEY = f.read()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY, cache_discovery=False)
    return youtube


def get_comment_threads(youtube, video_id, comments=[], token=""):
    results = youtube.commentThreads().list(
        part="snippet",
        pageToken=token,
        videoId=video_id,
        textFormat="plainText"
    ).execute()

    for item in results["items"]:
        comment = item["snippet"]["topLevelComment"]
        text = comment["snippet"]["textDisplay"]
        comments.append(text)

    if "nextPageToken" in results:
        return get_comment_threads(youtube, video_id, comments, results["nextPageToken"])
    else:
        return comments


def get_video_snippet(youtube, video_id):
    request = youtube.videos().list(
        part="snippet, statistics",
        id=video_id
    )
    response = request.execute()
    return response['items'][0]


def sentiment_analysis(comments):
    df = pd.DataFrame(data=comments, columns=['comments'])

    # polarity
    df['polarity'] = df['comments'].apply(
        lambda x: float(TextBlob(x).sentiment[0]))

    # sentiment
    for index, row in df.iterrows():
        if row['polarity'] > 0.05:
            df.loc[index, ['sentiment']] = 'positive'
        if row['polarity'] < -0.05:
            df.loc[index, ['sentiment']] = 'negative'
        if row['polarity'] == 0:
            df.loc[index, ['sentiment']] = 'neutral'

    return df


def sentiment_analysis_value_counts(df):
    d = {'count': df.sentiment.value_counts().values.tolist(
    ), 'sentiment': df.sentiment.value_counts().index.tolist()}
    return pd.DataFrame(data=d)
