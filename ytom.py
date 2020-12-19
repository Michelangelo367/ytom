import os
import googleapiclient.discovery
import pandas as pd
from textblob import TextBlob


def get_comments(video_id):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyD4cZ8-G16DENJzsuKHn4kPdZLQ9YbVccE"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    results = youtube.commentThreads().list(
        part="snippet",
        maxResults=100,
        videoId=video_id,
        textFormat="plainText").execute()

    totalResults = 0
    totalResults = int(results["pageInfo"]["totalResults"])
    count = 0
    nextPageToken = ''
    comments = []
    further = True
    first = True

    while further:
        halt = False
        if first == False:
            try:
                results = youtube.commentThreads().list(
                    part="snippet",
                    maxResults=100,
                    videoId=video_id,
                    textFormat="plainText",
                    pageToken=nextPageToken).execute()
                totalResults = int(results["pageInfo"]["totalResults"])
            except HttpError:
                print("An HTTP error occurred:\n", e.resp.status, e.content)
                halt = True

        if halt == False:
            count += totalResults
            for item in results["items"]:
                text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(text)

            if totalResults < 100:
                further = False
                first = False

            else:
                further = True
                first = False
                try:
                    nextPageToken = results["nextPageToken"]
                except KeyError:
                    print("An KeyError error occurred:", e)
                    further = False

    return comments


def sentiment_analysis(comments):
    df = pd.DataFrame(data=comments, columns=['text'])

    # polarity
    df['polarity'] = df['text'].apply(
        lambda x: float(TextBlob(x).sentiment[0]))

    # sentiment
    for index, row in df.iterrows():
        if row['polarity'] > 0:
            df.loc[index, ['sentiment']] = 'positive'
        if row['polarity'] < 0:
            df.loc[index, ['sentiment']] = 'negative'
        if row['polarity'] == 0:
            df.loc[index, ['sentiment']] = 'neutral'

    d = {'count': df.sentiment.value_counts().values.tolist(
    ), 'sentiment': df.sentiment.value_counts().index.tolist()}
    return pd.DataFrame(data=d)
