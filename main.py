from unicodedata import category

import requests
from bs4 import BeautifulSoup
import streamlit as st

from CurrentsAPI.CurrentsAPI import CurrentsAPI

if __name__ == '__main__':
    # Get the latest news and categories
    current_api = CurrentsAPI(api_key="hjIDNV6UwRv5-hq_tfDJzuALpIN7ay0mPxuvwuMbRj-wn4IK")
    categories = current_api.get_categories()
    news_response = current_api.get_latest_news()

    st.title("Latest News")
    option = st.selectbox(
        "Select a category of News?",
        categories,
    )

    st.write("You selected:", option)

    container = st.container()
    with container:
        for article in news_response.news:
            article_container = st.container(border=True)
            with article_container:
                st.image(article.image, caption="Sunrise by the mountains")
                st.subheader(article.title)
                st.write(article.description)
                st.write(f"Author: {article.author}")
                st.write(f"Published on: {article.published}")
                st.write(f"[Read more]({article.url})")





