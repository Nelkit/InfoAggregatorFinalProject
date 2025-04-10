from typing import List

from TheGuardianAPI.GuardianArticle import GuardianArticle

class GuardianResponse:
    def __init__(self,
                 status: str,
                 userTier: str,
                 total: int,
                 startIndex: int,
                 pageSize: int,
                 currentPage: int,
                 pages: int,
                 orderBy: str,
                 results: List[GuardianArticle]):
        self.status = status
        self.userTier = userTier
        self.total = total
        self.startIndex = startIndex
        self.pageSize = pageSize
        self.currentPage = currentPage
        self.pages = pages
        self.orderBy = orderBy
        self.results = results

    def __repr__(self):
        return f"ResponseData(status={self.status}, total_results={self.total})"


class ApiResponse:
    def __init__(self, response: GuardianResponse):
        self.response = response

    def __repr__(self):
        return f"ApiResponse(status={self.response.status})"