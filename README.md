# YTOM ~ YouTube Opinion Mining
> Automatically understand the feelings and emotions from YouTube Comments.

This project creates a website on which users can fill in the link of a YouTube video to extract the comments, analyze their feelings, and finally sort them according to the sentiment.

This project has an educative purpose of understanding how to create and deploy a Python project with the YouTube Data API v3, Streamlit, and Heroku.

https://youtube-opinion-mining.herokuapp.com/

![](ytom_preview.gif)

## Installation

Install libraries:

```sh
pip3 install -r requirements.txt
```

Create .env file:

```sh
# create an .env file and add your API key as shown with .env-sample
# don't forget to add your API key in your Heroku config vars before deploying with Heroku
YOUTUBE_SECRET_KEY=Some value
```

Run on localhost with Streamlit:

```sh
streamlit run app.py
```

Deploy with Heroku:

```sh
# You need to download Heroku CLI and create an account
heroku login
heroku create
git push heroku main
```

## Usage example

This product does not have an apparent use in its current form. It is currently a proof-of-concept of the feasibility of quickly analyzing the YouTube comments of any video. However, it is possible to envision a more advanced implementation to propose to brands partnering on YouTube videos to precisely target the words that quote the brand and evaluate the users' emotion towards it.

## Release History

* 0.1.0
    * The first release
    * `sentiment_analysis()` and `sentiment_overview()`
* 0.0.6
    * Heroku and secret_key
* 0.0.5
    * app.py
* 0.0.4
    * sentiment_analysis() & sentiment_analysis()
* 0.0.3
    * test_is_youtube_url() & test_get_video_id_from_youtube_url()
* 0.0.2
    * is_youtube_url() & get_video_id_from_youtube_url()
* 0.0.1
    * YouTube API & get_comment_threads()

## Meta

Loïc Rouiller-Monay – [@loicrm](https://twitter.com/loicrm)

[https://github.com/loicrouillermonay](https://github.com/loicrouillermonay/)