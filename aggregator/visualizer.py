import plotly.express as px
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

        # Step 1: Count articles per day
        article_calendar = Counter()
        for article in articles:
            if article.date:
                date = datetime.fromisoformat(article.date.replace("Z", "")).date()
                article_calendar[date] += 1
        
        # Step 2: Prepare data for heatmap
        calendar_data = pd.DataFrame.from_dict(article_calendar, orient='index', columns=['count'])
        calendar_data.index = pd.to_datetime(calendar_data.index)
        calendar_data = calendar_data.resample('D').sum().fillna(0)  # Fill missing days with 0
        
        # Step 3: Prepare data for monthly aggregation with year
        calendar_data['month'] = calendar_data.index.month
        calendar_data['month_name'] = calendar_data.index.strftime('%B')
        calendar_data['year'] = calendar_data.index.year
        
        # Create a proper dataframe for monthly data
        monthly_data = []
        for (year, month_name), group in calendar_data.groupby(['year', 'month_name']):
            monthly_data.append({
                'Year': int(year),  # Force year to be integer
                'Month': month_name,
                'Number of Articles': group['count'].sum()
            })
        
        monthly_df = pd.DataFrame(monthly_data)
        
        # Sort months in correct order
        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December']
        monthly_df['Month'] = pd.Categorical(monthly_df['Month'], categories=month_order, ordered=True)
        monthly_df = monthly_df.sort_values(['Year', 'Month'])
        
        # Create the plot
        fig = px.bar(
            monthly_df,
            x='Month',
            y='Number of Articles',
            color='Year',  # Different color for each year
            barmode='group',
            title="Number of Articles per Month by Year",
            color_discrete_map={str(year): px.colors.qualitative.Set3[i % len(px.colors.qualitative.Set3)] for i, year in enumerate(sorted(monthly_df['Year'].unique()))}  # Assign distinct colors for each year
        )
        
        # Update layout for better presentation
        fig.update_layout(
            title="Number of Articles per Month by Year",
            xaxis_title="Month",
            yaxis_title="Number of Articles",
            legend_title="Year",
            showlegend=True,
            xaxis={'categoryorder': 'array', 'categoryarray': month_order}
        )
        
        return fig
    # 4. Numero de palabras por artículo
    def number_of_words_plot(self, articles, max_articles=40):
        # Limit the number of articles to the specified maximum, ensuring 10 from each source if possible
        source_groups = {}
        for article in articles:
            source = article.source if hasattr(article, 'source') and article.source else "Unknown"
            if source not in source_groups:
                source_groups[source] = []
                source_groups[source].append(article)

        # Select up to 10 articles per source
        articles_to_plot = []
        # Flatten the articles list and limit to the specified maximum
        articles_to_plot = articles[:max_articles]

        # Calculate the number of words for each article and extract the first word of the title
        word_counts = [
            {
            "Article": " ".join(article.title.split()[:2]) if hasattr(article, 'title') and article.title else f"Article {i+1}",
            "Word Count": len(article.body.split()) if hasattr(article, 'body') and article.source == "bbc" else len(article.content.split()) if hasattr(article, 'content') else 0,
            "Source": article.source if hasattr(article, 'source') and article.source else "Unknown"
            }
            for i, article in enumerate(articles_to_plot)
        ]

        # Convert to DataFrame for plotting
        df = pd.DataFrame(word_counts)

        # Create the bar chart
        fig = px.bar(
            df,
            y='Article',
            x='Word Count',
            color='Source',
            title=f"Number of Words per Article",
            labels={'Article': 'Article', 'Word Count': 'Number of Words', 'Source': 'Source'},
            color_discrete_sequence=px.colors.qualitative.Set2,
            orientation='h'  # Horizontal bar chart
        )

        # Additional layout customization
        fig.update_layout(
            yaxis_title="Article",
            xaxis_title="Number of Words",
            height=600,
            margin=dict(l=150),  # Add left margin for longer article titles
            showlegend=True
        )

        return fig
