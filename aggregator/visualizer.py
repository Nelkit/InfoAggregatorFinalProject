import plotly.express as px

class NewsVisualizer:
    def source_distribution_plot(self, df):
        fig = px.bar(df, x='source', title="Distribution by source")
        return fig

    def articles_by_day_plot(self, df):
        fig = px.bar(df, x='source', title="Articles by day")
        return fig