from datetime import datetime

import streamlit as st
from aggregator.api_client import APIClient
from aggregator.scraper import ArticleScraper
from aggregator.processor import NewsProcessor
from aggregator.visualizer import NewsVisualizer

class AggregatorApp:
	def __init__(self):
		self.limit_selected = None
		self.source_selected = None
		self.category_selected = None
		self.api_client = APIClient()
		self.scraper = ArticleScraper()
		self.processor = NewsProcessor()
		self.visualizer = NewsVisualizer()
		self.articles = []

	'''
	Renderiza la barra lateral para la entrada del usuario
	'''
	def render_sidebar(self):
		st.sidebar.title("Search Filters")

		categories = self.api_client.fetch_categories()
		sources = self.api_client.fetch_sources()

		self.category_selected = st.sidebar.selectbox("Category", categories)
		self.source_selected = st.sidebar.selectbox("Source", sources)
		self.limit_selected = st.sidebar.slider("Number of Articles", 5, 50, 10)

	''' Renderiza la ventana de detalles del artículo cuando se hace clic en `🔗 Read More`'''
	@st.dialog("News Details", width="large")
	def render_article_detail(self):
		article_id = st.session_state.get('article_id')
		if article_id:
			#TODO Implementar la función de detalles del artículo
			article = self.api_client.fetch_article_details(article_id)
			st.write(f"### {article['title']}")
			st.write(f"**Source:** {article['source']} | **Date:** {article['date']}")
			st.markdown(article['content'], unsafe_allow_html=True)

	''' Renderiza cada artículo en la sección de noticias más recientes '''
	def render_article(self, article):
		with st.container(border=True):
			st.markdown(f"### {article['title']}")
			st.markdown(f"**Fuente:** {article['source']} | **Fecha:** {article['date']}")
			st.markdown(article['summary'])
			if st.button("🔗 Read More", key=article['id']):
				st.session_state['article_id'] = article['id']
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
		user_input = {
			"category": self.category_selected,
			"source": self.source_selected,
			"limit": self.limit_selected
		}
		source = user_input.get("source", "all")
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
		tab1, tab2 = st.tabs(["📰 Latest News", "📈 Visualization"])
		user_input = {
			"category": self.category_selected,
			"source": self.source_selected,
			"limit": self.limit_selected
		}
		# Se obtienen los artículos de la API
		articles = self.api_client.fetch_articles(user_input)
		# Se enriquecen los artículos con información adicional aca se pueden agregar más funciones
		enriched = self.scraper.enrich_articles(articles)
		# Se limpian los artículos para su visualización por si tienen algun elemento no deseado
		self.articles = self.processor.clean(enriched)

		# Se llama las funciones de renderizado para cada pestaña
		with tab1:
			self.render_latest_news()

		with tab2:
			self.render_visualizations()

		# Se llama a la función de renderizado del pie de página
		self.render_footer()
