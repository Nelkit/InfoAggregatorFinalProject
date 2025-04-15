import plotly.express as px

class NewsVisualizer:
    #TODO Implementar los siguientes graficos
    # 1. Gráfico de distribución por fuente
    # 2. Nube de Palabras por noticia
    # 3. Gráfico de artículos por día (cuantos artículos se publicaron por día)
    # 4. Numero de palabras por artículo
    def source_distribution_plot(self, articles):
        df = [{"source": "source1", "count": 10}, {"source": "source2", "count": 20}]
        fig = px.bar(df, x='source', title="Distribution by source")
        return fig

    def articles_by_day_plot(self, articles):
        df = [{"source": "source1", "count": 10}, {"source": "source2", "count": 20}]
        fig = px.bar(df, x='source', title="Articles by day")
        return fig