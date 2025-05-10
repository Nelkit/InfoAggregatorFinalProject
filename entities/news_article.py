from typing import Optional, Dict, Any
from dataclasses import dataclass, fields


class NewsArticle:
    """
    Base class for news articles that provides common functionality and attributes
    for different news sources.
    """

    def __init__(self, title: str, feature_image_url: str, content: Optional[str], summary: str, 
                 author: Optional[str], source: str, date: str, url: str):
        """
        Initialize a news article with its basic attributes.

        Args:
            title (str): The title of the article
            feature_image_url (str): URL of the main article image
            content (Optional[str]): The full article content
            summary (str): A brief summary of the article
            author (Optional[str]): The article's author
            source (str): The news source (e.g., "BBC News", "The Guardian")
            date (str): Publication date
            url (str): URL of the article
        """
        self.title = title
        self.feature_image_url = feature_image_url
        self.content = content
        self.summary = summary
        self.author = author
        self.source = source
        self.date = date
        self.url = url

    def __repr__(self):
        """Returns a string representation of the article."""
        return f"{self.__class__.__name__}(title={self.title!r}, author={self.author!r}, date={self.date!r})"

    def get_id(self):
        """Returns a unique identifier for the article based on its URL."""
        return f"{self.url}"

    def get_article_preview_md(self, limit: int = 100):
        """
        Generates a markdown preview of the article.

        Args:
            limit (int, optional): Maximum length of the summary. Defaults to 100.

        Returns:
            str: Markdown formatted article preview
        """
        title = f"### {self.title}"
        subtitle = f"**Source:** {self.source} | **Date:** {self.date}"
        return f"{title} \n {subtitle} \n\n {self.__get_summary_md__(limit=limit)}"

    def get_article_full_md(self):
        """
        Generates the full article content in markdown format.

        Returns:
            str: Markdown formatted full article
        """
        subtitle = f"**Source:** {self.source} | **Date:** {self.date}"
        return f"{subtitle} \n {self.content}"

    def __get_summary_md__(self, limit: int = 100):
        """
        Generates a truncated summary in markdown format.

        Args:
            limit (int, optional): Maximum length of the summary. Defaults to 100.

        Returns:
            str: Truncated summary with ellipsis
        """
        if self.summary is None:
            if self.content:
                self.summary = self.content[:limit] + "..."
        else:
            self.summary = self.summary[:limit] + "..."
        return f"{self.summary}"


class TheGuardianArticle(NewsArticle):
    """
    Class representing an article from The Guardian news source.
    Extends the base NewsArticle class with Guardian-specific attributes.
    """

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
        """
        Initialize a Guardian article with its specific attributes.

        Args:
            id (str): Article identifier
            type (str): Article type
            sectionId (str): Section identifier
            sectionName (str): Section name
            webPublicationDate (str): Publication date
            webTitle (str): Article title
            webUrl (str): Article URL
            apiUrl (str): API URL
            fields (dict): Additional article fields
            isHosted (bool): Whether the article is hosted
            pillarId (Optional[str]): Pillar identifier
            pillarName (Optional[str]): Pillar name
        """
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
        self.fields = fields  

    def __repr__(self):
        """Returns a string representation of the Guardian article."""
        return f"{self.__class__.__name__}(title={self.title!r}, section={self.sectionName!r}, date={self.date!r})"


class NYTArticle(NewsArticle):
    """
    Class representing an article from The New York Times.
    Extends the base NewsArticle class with NYT-specific attributes.
    """

    def __init__(
        self, 
        abstract: str,
        byline: dict,  
        document_type,
        headline: dict, 
        _id, 
        keywords,  
        multimedia: Dict[str, Any],  
        news_desk, 
        print_page,
        print_section,
        pub_date: str, 
        section_name,
        snippet,
        source: str, 
        subsection_name,
        type_of_material,
        uri,
        web_url: str,
        word_count
    ):
        """
        Initialize a New York Times article with its specific attributes.

        Args:
            abstract (str): Article summary
            byline (dict): Author information
            document_type: Type of document
            headline (dict): Headline information
            _id: Article identifier
            keywords: Article keywords
            multimedia (Dict[str, Any]): Media information
            news_desk: News desk information
            print_page: Print page number
            print_section: Print section
            pub_date (str): Publication date
            section_name: Section name
            snippet: Article snippet
            source (str): News source
            subsection_name: Subsection name
            type_of_material: Material type
            uri: Article URI
            web_url (str): Article URL
            word_count: Word count
        """
        super().__init__(
            title=str(headline.get('print_headline')), 
            feature_image_url=multimedia.get('default', {}).get('url'), 
            content=None, 
            summary=abstract, 
            author=byline.get('original'), 
            source="New York Times", 
            date=pub_date, 
            url=web_url
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
    """
    Class representing an article from BBC News.
    Extends the base NewsArticle class with BBC-specific attributes.
    """

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
        body: str = ""
    ):
        """
        Initialize a BBC article with its specific attributes.

        Args:
            uuid (str): Unique identifier
            title (str): Article title
            description (str): Article description
            url (str): Article URL
            image_url (str): Image URL
            published_at (str): Publication date
            source (str): News source
            content (str): Article content
            body (str, optional): Full article body. Defaults to empty string.
        """
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
        self.body = body

    def get_article_full_md(self):
        """
        Generates the full article content in markdown format.
        Uses body content if available, otherwise falls back to content.

        Returns:
            str: Markdown formatted full article
        """
        subtitle = f"**Source:** {self.source} | **Date:** {self.date}"
        return f"{subtitle} \n\n {self.body or self.content}"

    @staticmethod
    def from_dict(article: dict) -> "BBCArticle":
        """
        Creates a BBCArticle instance from a dictionary.

        Args:
            article (dict): Dictionary containing article data

        Returns:
            BBCArticle: New BBCArticle instance
        """
        valid_fields = {
            "uuid", "title", "description", "content", "url", "image_url", 
            "published_at", "source", "body"
        }
        filtered = {k: article.get(k, "") for k in valid_fields}
        return BBCArticle(**filtered)


class GNewsArticle(NewsArticle):
    """
    Class representing an article from GNews.
    Extends the base NewsArticle class with GNews-specific attributes.
    """

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
        """
        Initialize a GNews article with its specific attributes.

        Args:
            title (str): Article title
            description (str): Article description
            content (str): Article content
            url (str): Article URL
            image (str): Image URL
            publishedAt (str): Publication date
            source (str): News source
        """
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
        self.title = title
        self.description = description
        self.content = content
        self.url = url
        self.image = image

    def __repr__(self):
        """Returns a string representation of the GNews article."""
        return f"{self.__class__.__name__}(title={self.title!r}, date={self.date!r})"
