# YTOM ~ YouTube Opinion Mining
> Automatically understand the feelings and emotions from YouTube Comments.

This project creates a website on which users can fill in the link of a YouTube video to extract the comments, analyze their feelings, and finally sort them according to the sentiment.

This project has an educative purpose of understanding how to create and deploy a Python project with the YouTube Data API v3, Streamlit, and Heroku.

https://youtube-opinion-mining.herokuapp.com/

![](header.png)

## Installation

Install libraries:

```sh
pip3 install -r requirements.txt
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
git add .
git commit -m "heroku"
git push heroku main
```

## Usage example

This product does not have an apparent use in its current form. It is currently a proof-of-concept of the feasibility of quickly analyzing the YouTube comments of any video. However, it is possible to envision a more advanced implementation to propose to brands partnering on YouTube videos to precisely target the words that quote the brand and evaluate the users' emotion towards it.

## Release History

* 0.1.0
    * The first proper release
    * `sentiment_analysis()` and `sentiment_overview()`
* 0.0.1
    * Work in progress

## Meta

Loïc Rouiller-Monay – [@loicrm](https://twitter.com/loicrm) – loicrouillermonay@gmail.com

Distributed under the XYZ license. See ``LICENSE`` for more information.

[https://github.com/loicrouillermonay](https://github.com/loicrouillermonay/)

## Contributing

1. Fork it (<https://github.com/loicrouillermonay/ytom/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request