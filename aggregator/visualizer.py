import plotly.express as px
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from entities.news_article import NewsArticle

class NewsVisualizer:
    #TODO Implementar los siguientes graficos
    # 1. Gráfico de distribución por fuente | Saantiago
    # 2. Nube de Palabras por noticia  | Juan David
    # 3. Gráfico de artículos por día (cuantos artículos se publicaron por día) | Nelkit
    # 4. Numero de palabras por artículo | Luis

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
        fig, _ = plt.subplots(figsize = (10, 8))
        sns.despine(fig)
        sns.barplot(
            data = df,
            y = 'source',
            x = 'total articles',
            hue = 'source',
            palette = 'Blues_r'
        )
        return fig

    # 2. Nube de Palabras por noticia
    def word_cloud_plot(self, articles):
        df = [{"source": "source1", "count": 10}, {"source": "source2", "count": 20}]
        fig = px.bar(df, x='source', title="Word Cloud in News")
        return fig

    # 3. Gráfico de artículos por día
    def articles_by_day_plot(self, articles):
        days = [datetime.fromisoformat(ts.date.replace("Z", "+00:00")).day for ts in articles]

        days_series = pd.Series(days)

        day_counts = days_series.value_counts()
        df = day_counts.reset_index()
        df.columns = ['day', 'count']
        print(df)

        fig = px.scatter(df, x='day', y='count', title='Articles Count by Day of the Month', size='count')
        fig.update_xaxes(dtick=2)
        return fig

    # 4. Numero de palabras por artículo
    def number_of_words_plot(self, articles):
        df = [{"source": "source1", "count": 10}, {"source": "source2", "count": 20}]
        fig = px.bar(df, x='source', title="Number of words per article")
        return fig