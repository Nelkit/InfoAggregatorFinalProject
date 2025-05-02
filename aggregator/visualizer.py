import plotly.express as px
from datetime import datetime
import pandas as pd
import seaborn as sns
from entities.news_article import NewsArticle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from aggregator.processor import NewsProcessor
import streamlit as st


class NewsVisualizer:
    #TODO Implementar los siguientes graficos
    # 1. Gráfico de distribución por fuente | Saantiago
    # 2. Nube de Palabras por noticia  | Juan David DONE
    # 3. Gráfico de artículos por día (cuantos artículos se publicaron por día) | Nelkit
    # 4. Numero de palabras por artículo | Luis

    def __init__(self):
        self.processor = NewsProcessor()

    # 1. Gráfico de distribución por fuente
    def source_distribution_plot(self, articles : list[NewsArticle]):
        sources = [a.source for a in articles]
        source_counter = {}
        for s in sources:
            if s in source_counter.keys():
                source_counter[s] += 1
            else:
                source_counter[s] = 1
        df = pd.DataFrame(data = zip(source_counter.keys(), source_counter.values()), columns = ['source', 'total articles']).sort_values(by = 'total articles', ascending=False)
        fig, _ = plt.subplots(figsize = (10, 6))
        sns.despine(fig)
        sns.barplot(
            data = df,
            y = 'source',
            x = 'total articles',
            hue = 'source',
            palette = 'Blues_r'
        )
        return fig

    # 2. WordCloud by source and category  
    def word_cloud_plot(self, articles):
        # Combine all summaries
        merge_text = " ".join(article.summary for article in articles if article.summary)
        clean_text = self.processor.clean_articles_for_wordcloud(merge_text)

        if not clean_text.strip():
            st.warning("There is no text available to generate the word cloud.")
            return None

        # Generate WordCloud
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            min_font_size=10,
            max_font_size=100,
            scale=2
        ).generate(clean_text)

        # Unique words found
        unique_words = len(wordcloud.words_)

        if unique_words < 3:
            st.warning("Not enough unique words to generate a meaningful word cloud.")
            return None

        # Crete graph
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud.to_array(), interpolation='bilinear')
        ax.axis('off')  # hide axis

    
        return fig

    # 3. Gráfico de artículos por día
    def articles_by_day_plot(self, articles):
        days = [datetime.fromisoformat(ts.date.replace("Z", "+00:00")).day for ts in articles]

        days_series = pd.Series(days)

        day_counts = days_series.value_counts()
        df = day_counts.reset_index()
        df.columns = ['day', 'count']

        fig = px.scatter(df, x='day', y='count', title='Articles Count by Day of the Month', size='count')
        fig.update_xaxes(dtick=2)
        return fig

    # 4. Numero de palabras por artículo
    def number_of_words_plot(self, articles):
        df = [{"source": "source1", "count": 10}, {"source": "source2", "count": 20}]
        fig = px.bar(df, x='source', title="Number of Words per Article")
        return fig