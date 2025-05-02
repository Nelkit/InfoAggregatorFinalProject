from typing import Optional, Dict, Any
from dataclasses import dataclass, fields


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
        return f"{title} \n {subtitle} \n\n {self.__get_summary_md__(limit=limit)}"

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

class NYTArticle(NewsArticle):
    def __init__(
        self, 
        abstract : str, # summary of the news
        byline : dict, # dictionary with the authors
        document_type,
        headline : dict, # dictionary with the following keys [main, kicker, print_headline]
        _id, 
        keywords, # dictionary with the following keys [name, value, rank]
        multimedia : Dict[str, Any], # dictionary with the following keys [caption, credit, default, thumbnail]
        # default has the following keys [url, height, width]
        # thumbnail has the following keys [url, height, width]
        news_desk, 
        print_page,
        print_section,
        pub_date : str, # self explanatory
        section_name,
        snippet,
        source : str, 
        subsection_name,
        type_of_material,
        uri,
        web_url : str,
        word_count
    ):
        super().__init__(
            # using sample querys, the enpoint is not getting this field
            title = str(headline.get('print_headline')), 
            feature_image_url = multimedia.get('default', {}).get('url'), 
            content = None, 
            summary = abstract, 
            author = byline.get('original'), 
            source = "New York Times", 
            date = pub_date, 
            url = web_url
        )
        self.byline = byline
        self.document_type = document_type
        self.headline = headline
        self._id = _id
        self.keywords = keywords
        self.multimedia = multimedia
        self.news_desk = news_desk
        self.print_page = print_page
        self.print_section = print_section
        self.section_name = section_name
        self.snippet = snippet
        self.subsection_name = subsection_name
        self.type_of_material = type_of_material
        self.uri = uri
        self.word_count = word_count
        self.main = self.headline.get('main')
        self.kicker = self.headline.get('kicker')
        

class BBCArticle(NewsArticle):
    def __init__(
        self, 
        uuid: str, 
        title: str, 
        description: str, 
        url: str, 
        image_url: str, 
        published_at: str, 
        source: str,
        content: str,
        body: str = ""  # Add body here
    ):
        super().__init__(
            title=title,
            content=description,
            summary=description,
            author=None,
            source=source,
            date=published_at,
            url=url,
            feature_image_url=image_url
        )
        self.uuid = uuid
        self.image_url = image_url
        self.body = body  # Store the body text

    def get_article_full_md(self):
        subtitle = f"**Source:** {self.source} | **Date:** {self.date}"
        return f"{subtitle} \n\n {self.body or self.content}"
  

    @staticmethod
    def from_dict(article: dict) -> "BBCArticle":
        valid_fields = {
            "uuid", "title", "description", "content", "url", "image_url", "published_at", "source", "body"
        }
        filtered = {k: article.get(k, "") for k in valid_fields}
        return BBCArticle(**filtered)

class GNewsArticle(NewsArticle):
    def __init__(
        self,
        title: str,
        description: str,
        content: str,
        url: str,
        image: str,
        publishedAt: str,
        source: str,
    ):
        super().__init__(
            date=publishedAt, 
            source="GNews",
            title=title,
            feature_image_url=image,
            content=content, 
            summary=description,
            author=None,
            url=url    
        )

        self.title=title
        self.description=description
        self.content=content
        self.url=url
        self.image=image


    def __repr__(self):
        return f"{self.__class__.__name__}(title={self.title!r}, date={self.date!r})"
