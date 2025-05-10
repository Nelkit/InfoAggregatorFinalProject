from datetime import datetime
import streamlit as st
from aggregator.api_client import GNewsApi, TheGuardianApi, BBCApi, NYTNewsApi, APIClient
from aggregator.scraper import ArticleScraper
from aggregator.processor import NewsProcessor
from aggregator.visualizer import NewsVisualizer
from entities.news_article import NewsArticle
from entities.user_input import UserInput


class AggregatorApp:
	"""
	Main application class for the News Aggregator.
	Handles the integration of multiple news sources and provides a Streamlit-based UI.
	"""
	def __init__(self):
		# Initialize state variables
		self.source_selected = None
		self.category_selected = None
		
		# Initialize API clients with their respective credentials
		self.api_client = APIClient(api_key="", base_url="")
		self.the_guardian_api = TheGuardianApi(
			api_key="f6f96e89-7097-46c0-9266-5d2001202068",
			base_url="https://content.guardianapis.com/",
		)
		self.bbc_api = BBCApi(
			api_key="bb59763f972342a28391325a180928c3",
			base_url="https://newsapi.org/v2/top-headlines/"
		)
		self.nyt_api = NYTNewsApi(
			api_key="zv2dhOM3UJMipTtusff6f1dD3GSxnEXe",
			base_url="https://api.nytimes.com/svc/search/v2/"
		)
		self.gnews_api = GNewsApi(
			api_key="83eb364c60aa9cad8a67cf93ca2bde9d",
			base_url="https://GNews.io/api/v4/",
		)
		
		# Initialize processors and visualizers
		self.processor = NewsProcessor()
		self.visualizer = NewsVisualizer()
		self.articles = []

	def get_article_details(self, article_url: str) -> NewsArticle:
		"""
		Retrieves article details from the internal memory based on URL.
		
		Args:
			article_url (str): The URL of the article to find
			
		Returns:
			NewsArticle: The found article object
			
		Raises:
			ValueError: If the article is not found in internal memory
		"""
		for article in self.articles:
			if article.url == article_url:
				return article
		raise ValueError("Article not found in internal memory.")

	''' Renders the sidebar with search filters for categories and news sources. '''

	def render_sidebar(self):
		"""
		Renders the sidebar with search filters for categories and news sources.
		"""
		st.sidebar.title("Search Filters")

		categories = self.api_client.fetch_categories()
		sources = self.api_client.fetch_sources()

		self.category_selected = st.sidebar.selectbox("Category", categories)
		self.source_selected = st.sidebar.selectbox("Source", sources)

	''' Renders the article detail window when clicking on '🔗 Read More' '''

	@st.dialog("News Details", width="large")
	def render_article_detail(self):
		"""
		Renders the article detail dialog when 'Read More' is clicked.
		Displays the full article content with images and formatting.
		"""
		with st.spinner("Fetching article details..."):
			article_id = st.session_state.get('article_id')
			article_source = st.session_state.get('source')

			if article_id and article_source:
				article = self.get_article_details(article_id)

				if article:
					st.header(article.title)
					if article.feature_image_url:
						st.image(article.feature_image_url, caption=article.title)
					st.markdown(article.get_article_full_md(), unsafe_allow_html=True)
					st.markdown(article.url)

	''' Renders each article in the latest news section '''

	def render_article(self, article: NewsArticle):
		"""
		Renders a single article preview in the latest news section.
		
		Args:
			article (NewsArticle): The article object to render
		"""
		with st.container(border=True):
			st.markdown(
				article.get_article_preview_md(limit=200),
				unsafe_allow_html=True
			)
			if st.button("🔗 Read More", key=article.get_id()):
				st.session_state['article_id'] = article.get_id()
				st.session_state['source'] = article.source

				self.render_article_detail()

	''' Renders the latest news section '''

	def render_latest_news(self):
		"""
		Renders the latest news section with all fetched articles.
		"""
		st.subheader("Latest News")
		for article in self.articles:
			self.render_article(article)

	''' Renders the data visualization section '''

	def render_visualizations(self):
		"""
		Renders data visualizations including source distribution, word cloud,
		articles by day, and word count analysis.
		"""
		st.subheader("Data Visualizations")

		col1, col2 = st.columns(2)
		col3, col4 = st.columns(2)

		with st.container(border=True):
			with col1:
				st.markdown("**Source Distribution Chart**")
				plot = self.visualizer.source_distribution_plot(self.articles)
				st.pyplot(plot)

			with col2:
				st.markdown("**Word Cloud by Category**")
				plot = self.visualizer.word_cloud_plot(self.articles)
				st.pyplot(plot)

			with col3:
				plot = self.visualizer.articles_by_day_plot(self.articles)
				st.plotly_chart(plot, key="chart_3")

			with col4:
				plot = self.visualizer.number_of_words_plot(self.articles)
				st.plotly_chart(plot, key="chart_4")


	''' Renders the footer with status and last update '''
	def render_footer(self):
		"""
		Renders the footer with status information and last update time.
		"""
		col1, col2 = st.columns(2)
		source = self.source_selected
		today = datetime.today()
		current_hour = today.strftime('%Y-%m-%d %H:%M:%S')
		col1_text = f"Status: {len(self.articles)} articles loaded. Source: {source}"
		col2_text = f"<div style='text-align: right'>Last updated: {current_hour}</div>"

		with col1:
			st.text(col1_text)

		with col2:
			st.markdown(col2_text, unsafe_allow_html=True)

	''' Renders the main application '''
	def run(self):
		"""
		Main method to run the News Aggregator application.
		Sets up the Streamlit interface and handles the main application flow.
		"""
		st.set_page_config(page_title="News Aggregator", layout="wide")
		st.title("News Aggregator")
		
		# Call the sidebar rendering function
		self.render_sidebar()

		# Create tabs for latest news and visualization
		tab1, tab2 = st.tabs(["📰 Latest News", "📈 Visualization"])
		user_input = UserInput(category=self.category_selected, source=self.source_selected)
		
		# Fetch articles from the API
		articles = []
		with st.spinner("Fetching news..."):
			# When "All" is selected, fetch articles from all APIs
			if self.source_selected == "All":
				theguarding_articles = self.the_guardian_api.fetch_articles(category=user_input.category)
				bbc_articles = self.bbc_api.fetch_articles(category=user_input.category, source=user_input.source)
				gnews_articles = self.gnews_api.fetch_articles(category=user_input.category)
				nyt_articles = self.nyt_api.fetch_articles(category=user_input.category)
				articles = (
						theguarding_articles +
						bbc_articles +
						gnews_articles +
						nyt_articles
				)
			# When "The Guardian" is selected, fetch articles from The Guardian API
			elif self.source_selected == "The Guardian":
				articles = self.the_guardian_api.fetch_articles(user_input.category)
			elif self.source_selected == "BBC News":
				articles = self.bbc_api.fetch_articles(user_input.source, user_input.category)
			elif self.source_selected == "New York Times":
				articles = self.nyt_api.fetch_articles(user_input.category)
			elif self.source_selected == "GNews":
				articles = self.gnews_api.fetch_articles(user_input.category)

			# Enrich articles with additional information through scraping
			# Additional functions can be added here
			scraper = ArticleScraper(articles)
			self.articles = scraper.get_enriched_articles()

			# Call rendering functions for each tab
			with tab1:
				self.render_latest_news()

			with tab2:
				self.render_visualizations()

		# Call the footer rendering function
		self.render_footer()