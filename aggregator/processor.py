from bs4 import BeautifulSoup
import re

class NewsProcessor:
    def clean_articles_for_wordcloud(self, html_text):
        # Step 1: Remove HTML tags using BeautifulSoup
        soup = BeautifulSoup(html_text, "html.parser")
        text = soup.get_text()

        # Step 2: Use regex to keep only words (letters), and optionally numbers
        clean_text = re.sub(r'[^A-Za-z\s]', '', text)  # Only letters and spaces
        # If you want to keep numbers too: use r'[^A-Za-z0-9\s]'

        # Step 3: Normalize spaces
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        return clean_text