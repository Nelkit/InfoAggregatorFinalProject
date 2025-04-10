import datetime
from typing import List

class NewsItem:
    def __init__(self, id: str, title: str, description: str, url: str, author: str, image: str, language: str, category: List[str], published: str):
        self.id = id
        self.title = title
        self.description = description
        self.url = url
        self.author = author
        self.image = image
        self.language = language
        self.category = category
        self.published = datetime.datetime.strptime(published, "%Y-%m-%d %H:%M:%S +0000")

    def __repr__(self):
        return f"NewsItem(id={self.id}, title={self.title}, author={self.author}, published={self.published})"

