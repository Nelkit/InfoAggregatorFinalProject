from typing import Optional

class NewsArticle:
    def __init__(self, title: str, feature_image_url: str, content: Optional[str], summary: str, author: Optional[str], source: str, date: str, url: str):
        self.title = title
        self.feature_image_url = feature_image_url
        self.content = content
        self.summary = summary
        self.author = author
        self.source = source
        self.date = date
        self.url = url

    def __repr__(self):
        return f"{self.__class__.__name__}(title={self.title!r}, author={self.author!r}, date={self.date!r})"

    def get_id(self):
        return f"{self.url}"

    def get_article_preview_md(self, limit: int = 100):
        title = f"### {self.title}"
        subtitle = f"**Source:** {self.source} | **Date:** {self.date}"
        return f"{title} \n {subtitle} \n {self.__get_summary_md__(limit=limit)}"

    def get_article_full_md(self):
        subtitle = f"**Source:** {self.source} | **Date:** {self.date}"
        return f"{subtitle} \n {self.content}"

    def __get_summary_md__(self, limit: int = 100):
        if self.summary is None:
            if self.content:
                self.summary = self.content[:limit] + "..."
        else:
            self.summary = self.summary[:limit] + "..."
        return f"{self.summary}"


class TheGuardianArticle(NewsArticle):
    def __init__(
        self,
        id: str,
        type: str,
        sectionId: str,
        sectionName: str,
        webPublicationDate: str,
        webTitle: str,
        webUrl: str,
        apiUrl: str,
        fields: dict,
        isHosted: bool,
        pillarId: Optional[str] = None,
        pillarName: Optional[str] = None
    ):
        super().__init__(
            title=webTitle,
            feature_image_url=fields.get('thumbnail'),
            content=fields.get('body'),
            summary=fields.get('body'),
            author=fields.get('byline'),
            source="The Guardian",
            date=webPublicationDate,
            url=webUrl
        )
        self.id = id
        self.type = type
        self.sectionId = sectionId
        self.sectionName = sectionName
        self.webUrl = webUrl
        self.apiUrl = apiUrl
        self.isHosted = isHosted
        self.pillarId = pillarId
        self.pillarName = pillarName
        self.fields = fields  # Puede ser útil para acceder a otros campos dinámicamente

    def __repr__(self):
        return f"{self.__class__.__name__}(title={self.title!r}, section={self.sectionName!r}, date={self.date!r})"