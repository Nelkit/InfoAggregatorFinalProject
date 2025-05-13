from datetime import datetime
import pandas as pd
import seaborn as sns
from entities.news_article import NewsArticle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from aggregator.processor import NewsProcessor
import streamlit as st
import plotly.express as px
from collections import Counter


class NewsVisualizer:
    """
    Class responsible for creating various visualizations of news article data.
    Provides methods for generating source distribution charts, word clouds,
    article timeline analysis, and word count analysis.
    """

    def __init__(self):
        self.processor = NewsProcessor()

    def source_distribution_plot(self, articles: list[NewsArticle]):
        """
        Creates a bar plot showing the distribution of articles by source.

        Args:
            articles (list[NewsArticle]): List of news articles to analyze

        Returns:
            matplotlib.figure.Figure: Bar plot showing article distribution by source
        """
        sources = [a.source for a in articles]
        source_counter = {}
        for s in sources:
            if s in source_counter.keys():
                source_counter[s] += 1
            else:
                source_counter[s] = 1
        df = pd.DataFrame(data=zip(source_counter.keys(), source_counter.values()), 
                         columns=['source', 'total articles']).sort_values(by='total articles', ascending=False)
        fig, _ = plt.subplots(figsize=(10, 6))
        sns.despine(fig)
        sns.barplot(
            data=df,
            y='source',
            x='total articles',
            hue='source',
            palette='Blues_r'
        )
        return fig

    def word_cloud_plot(self, articles):
        """
        Generates a word cloud visualization from article summaries.

        Args:
            articles (list[NewsArticle]): List of news articles to analyze

        Returns:
            matplotlib.figure.Figure: Word cloud visualization or None if insufficient data
        """
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

        # Check for sufficient unique words
        unique_words = len(wordcloud.words_)
        if unique_words < 3:
            st.warning("Not enough unique words to generate a meaningful word cloud.")
            return None

        # Create visualization
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud.to_array(), interpolation='bilinear')
        ax.axis('off')
        return fig

    def articles_by_day_plot(self, articles):
        """
        Creates a bar plot showing the number of articles published per month by year.

        Args:
            articles (list[NewsArticle]): List of news articles to analyze

        Returns:
            plotly.graph_objects.Figure: Interactive bar plot showing article distribution over time
        """
        # Count articles per day
        article_calendar = Counter()
        for article in articles:
            if article.date:
                date = datetime.fromisoformat(article.date.replace("Z", "")).date()
                article_calendar[date] += 1
        
        # Prepare data for analysis
        calendar_data = pd.DataFrame.from_dict(article_calendar, orient='index', columns=['count'])
        calendar_data.index = pd.to_datetime(calendar_data.index)
        calendar_data = calendar_data.resample('D').sum().fillna(0)
        
        # Aggregate data by month and year
        calendar_data['month'] = calendar_data.index.month
        calendar_data['month_name'] = calendar_data.index.strftime('%B')
        calendar_data['year'] = calendar_data.index.year
        
        # Create monthly aggregation
        monthly_data = []
        for (year, month_name), group in calendar_data.groupby(['year', 'month_name']):
            monthly_data.append({
                'Year': int(year),
                'Month': month_name,
                'Number of Articles': group['count'].sum()
            })
        
        monthly_df = pd.DataFrame(monthly_data)
        
        # Sort months chronologically
        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        monthly_df['Month'] = pd.Categorical(monthly_df['Month'], categories=month_order, ordered=True)
        monthly_df = monthly_df.sort_values(['Year', 'Month'])
        
        # Create interactive visualization
        fig = px.bar(
            monthly_df,
            x='Month',
            y='Number of Articles',
            color='Year',
            barmode='group',
            title="Number of Articles per Month by Year",
            color_discrete_map={str(year): px.colors.qualitative.Set3[i % len(px.colors.qualitative.Set3)] 
                              for i, year in enumerate(sorted(monthly_df['Year'].unique()))}
        )
        
        # Customize layout
        fig.update_layout(
            title="Number of Articles per Month by Year",
            xaxis_title="Month",
            yaxis_title="Number of Articles",
            height=600,
            legend_title="Year",
            showlegend=True,
            xaxis={'categoryorder': 'array', 'categoryarray': month_order}
        )
        
        return fig

    def number_of_words_plot(self, articles, max_articles=40):
        """
        Creates a horizontal bar plot showing the word count for each article.

        Args:
            articles (list[NewsArticle]): List of news articles to analyze
            max_articles (int, optional): Maximum number of articles to display. Defaults to 40.

        Returns:
            plotly.graph_objects.Figure: Interactive bar plot showing word counts per article
        """
        # Group articles by source
        source_groups = {}
        for article in articles:
            source = article.source if hasattr(article, 'source') and article.source else "Unknown"
            if source not in source_groups:
                source_groups[source] = []
                source_groups[source].append(article)

        # Select articles for visualization
        articles_to_plot = articles[:max_articles]

        # Calculate word counts for each article
        try:
            word_counts = [
                {
                    "Article": " ".join(article.title.split()[:2]) if hasattr(article, 'title') and article.title else f"Article {i+1}",
                    "Word Count": len(article.body.split()) if hasattr(article, 'body') and article.source == "bbc"
                                else len(article.content.split()) if hasattr(article, 'content') else 0,
                    "Source": article.source if hasattr(article, 'source') and article.source else "Unknown"
                }
                for i, article in enumerate(articles_to_plot)
            ]

            # Create visualization
            df = pd.DataFrame(word_counts)
            fig = px.bar(
                df,
                y='Article',
                x='Word Count',
                color='Source',
                title="Number of Words per Article",
                labels={'Article': 'Article', 'Word Count': 'Number of Words', 'Source': 'Source'},
                color_discrete_sequence=px.colors.qualitative.Set2,
                orientation='h'
            )

            # Customize layout
            fig.update_layout(
                yaxis_title="Article",
                xaxis_title="Number of Words",
                height=600,
                margin=dict(l=150),
                showlegend=True
            )

            return fig
        except Exception as e:
            st.error(f"Error generating word count plot: {e}")
            data = {'Article': ['None'], 'Word Count': [0]}
            return px.bar(
                data_frame=data,
                x='Word Count',
                y='Article',
                title="Word Count Plot",
                labels={'x': 'Number of Words', 'y': 'Article'},
                orientation='h'
            )
