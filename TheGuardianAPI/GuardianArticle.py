from typing import Optional
from datetime import datetime

class GuardianArticle:
	def __init__(self, id: str, type: str, sectionId: str, sectionName: str, webPublicationDate: str, webTitle: str, webUrl: str, apiUrl: str, fields: dict, isHosted: bool, pillarId: Optional[str], pillarName: Optional[str]):
		self.id = id
		self.type = type
		self.sectionId = sectionId
		self.sectionName = sectionName
		self.webPublicationDate = datetime.fromisoformat(webPublicationDate.replace("Z", "+00:00"))
		self.webTitle = webTitle
		self.webUrl = webUrl
		self.apiUrl = apiUrl
		self.isHosted = isHosted
		self.pillarId = pillarId
		self.pillarName = pillarName
		self.fields = fields

	def __repr__(self):
		return f"ResultItem(id={self.id}, title={self.webTitle}, date={self.webPublicationDate})"
