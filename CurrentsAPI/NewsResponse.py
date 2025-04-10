from typing import List
from CurrentsAPI.NewsItem import NewsItem

class NewsResponse:
    def __init__(self, status: str, news: List[NewsItem]):
        self.status = status
        self.news = news

    def __repr__(self):
        return f"NewsResponse(status={self.status}, news_count={len(self.news)})"