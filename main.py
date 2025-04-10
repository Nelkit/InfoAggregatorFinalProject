from typing import List
from unicodedata import category

import requests
from bs4 import BeautifulSoup
import streamlit as st

from TheGuardianAPI.GuardianArticle import GuardianArticle
from TheGuardianAPI.TheGuardianAPI import TheGuardianAPI

API_KEY = "f6f96e89-7097-46c0-9266-5d2001202068"

def fetch_latest_news(category: str = "world") -> List[GuardianArticle]:
    api = TheGuardianAPI(api_key=API_KEY)
    return api.get_latest_news(section=category, page_size=10).response.results

def render_news_ui(news: List[GuardianArticle]) -> None:
    st.container()  # inicial opcional
    for article in news:
        with st.container(border=True):
            st.subheader(article.webTitle)
            st.caption(article.sectionName)
            st.write(f"🗓 Published on: {article.webPublicationDate.strftime('%Y-%m-%d %H:%M:%S')}")
            st.markdown(f"[👉 Read more]({article.webUrl})")

def main():
    st.title("📰 Latest News")

    categories = [
        "world", "business", "environment", "politics",
        "education", "science", "technology"
    ]

    selected_category = st.selectbox("Select a news category:", categories)
    news = fetch_latest_news(selected_category)
    render_news_ui(news)

if __name__ == "__main__":
    main()







