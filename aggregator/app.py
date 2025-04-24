from datetime import datetime

import streamlit as st
from aggregator.api_client import APIClient, CNNNewsApi, TheGuardianApi
from aggregator.scraper import ArticleScraper
from aggregator.processor import NewsProcessor
from aggregator.visualizer import NewsVisualizer
from entities.news_article import NewsArticle
from entities.user_input import UserInput


class AggregatorApp:
	def __init__(self):
		self.source_selected = None
		self.category_selected = None
		self.api_client = APIClient(
			api_key="1835612ghjady763167823asd",
			base_url="https://localhost"
		)
		self.the_guardian_api = TheGuardianApi(
			api_key="f6f96e89-7097-46c0-9266-5d2001202068",
			base_url="https://content.guardianapis.com/",
		)
		self.cnn_news_api = CNNNewsApi(
			api_key="83eb364c60aa9cad8a67cf93ca2bde9d",
			base_url="https://gnews.io/api/v4/",
		)
		self.processor = NewsProcessor()
		self.visualizer = NewsVisualizer()
		self.articles = []

	def get_article_details(self, article_url: str) -> NewsArticle:
		for article in self.articles:
			if article.url == article_url:
				return article
		raise ValueError("Artículo no encontrado en la memoria interna.")

	'''
	Renderiza la barra lateral para la entrada del usuario
	'''

	def render_sidebar(self):
		st.sidebar.title("Search Filters")

		categories = self.api_client.fetch_categories()
		sources = self.api_client.fetch_sources()

		self.category_selected = st.sidebar.selectbox("Category", categories)
		self.source_selected = st.sidebar.selectbox("Source", sources)

	''' Renderiza la ventana de detalles del artículo cuando se hace clic en `🔗 Read More`'''

	@st.dialog("News Details", width="large")
	def render_article_detail(self):
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

	''' Renderiza cada artículo en la sección de noticias más recientes '''

	def render_article(self, article: NewsArticle):
		with st.container(border=True):
			st.markdown(
				article.get_article_preview_md(limit=200),
				unsafe_allow_html=True
			)
			if st.button("🔗 Read More", key=article.get_id()):
				st.session_state['article_id'] = article.get_id()
				st.session_state['source'] = article.source

				self.render_article_detail()

	''' Renderiza la sección de noticias más recientes '''

	def render_latest_news(self):
		for article in self.articles:
			self.render_article(article)

	''' Renderiza la sección de visualizaciones de datos '''

	def render_visualizations(self):
		st.subheader("Visualizaciones de Datos")

		# Se crean los contenedores para las visualizaciones
		with st.container(border=True):
			df = self.processor.clean(self.articles)
			plot = self.visualizer.source_distribution_plot(df)
			st.write(plot)

		# Se crean los contenedores para las visualizaciones
		with st.container(border=True):
			df = self.processor.clean(self.articles)
			plot = self.visualizer.articles_by_day_plot(df)
			st.write(plot)

	''' Renderiza el pie de página con el estado y la última actualización '''

	def render_footer(self):
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

	''' Renderiza la aplicación principal '''

	def run(self):
		st.set_page_config(page_title="News Aggregator", layout="wide")
		st.title("News Aggregator")
		# se llama a la función de renderizado de la barra lateral
		self.render_sidebar()

		# se crean las pestañas para las noticias más recientes y la visualización
		tab1, tab2 = st.tabs(["📈 Visualization", "📰 Latest News"])
		user_input = UserInput(category=self.category_selected, source=self.source_selected)
		# Se obtienen los artículos de la API
		articles = []
		with st.spinner("Fetching news..."):
			# cuando la fuente seleccionada es "All" se obtienen los artículos de ambas APIs
			if self.source_selected == "All":
				theguarding_articles = self.the_guardian_api.fetch_articles(user_input)
				dummy_articles = self.api_client.fetch_articles(user_input)
				articles = theguarding_articles + dummy_articles

			# cuando la fuente seleccionada es "The Guardian" se obtienen los artículos de la API de noticias
			elif self.source_selected == "The Guardian":
				articles = self.the_guardian_api.fetch_articles(user_input)

			# cuando la fuente seleccionada es "CNN" se obtienen los artículos de la Gnews API 
			elif self.source_selected == "CNN News":
				articles = self.cnn_news_api.fetch_articles(user_input)

			# Se enriquecen los artículos con información con scrapping adicional aca se pueden agregar más funciones
			scraper = ArticleScraper(articles)
			self.articles = scraper.enrich_articles()
			self.articles = scraper.get_enriched_articles()

			# Se llama las funciones de renderizado para cada pestaña
			with tab1:
				self.render_visualizations()

			with tab2:
				self.render_latest_news()

		# Se llama a la función de renderizado del pie de página
		self.render_footer()
