# Group Project Assignment: Information Aggregator with Web API and Scraping

## Python 🐍 Programming Subject

## Description  
This project challenges you to build an Information Aggregator using Web APIs and Web Scraping techniques. It emphasizes the application of object-oriented programming (OOP) and the implementation of unit testing to ensure a modular and reliable codebase. Additionally, a Graphical User Interface (GUI) is required to enhance user interaction and usability.

## Requirements  
List of dependencies and prerequisites needed to run the project.

- Python >= 3.x  
- Required libraries:
  - BeautifulSoup4  
  - Pandas  
  - Numpy  
  - Requests  
  - python-dotenv  
  - Streamlit  
  - *(See the `requirements.txt` file for additional necessary libraries.)*

## Installation  
1. Clone the repository:  
   ```sh
   git clone https://github.com/Nelkit/InfoAggregatorFinalProject.git
   cd InfoAggregatorFinalProject
   ```

2. Create and activate a virtual environment (optional but recommended):  
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:  
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the environment variables:**  
   Create a file named `.env` in the root directory of the project and add the following lines with your corresponding API keys and base URLs:

   ```
   THE_GUARDIAN_API_KEY=your_guardian_api_key
   THE_GUARDIAN_BASE_URL=https://content.guardianapis.com/

   BBC_API_KEY=your_bbc_api_key
   BBC_BASE_URL=https://newsapi.org/v2/top-headlines/

   NYT_API_KEY=your_nyt_api_key
   NYT_BASE_URL=https://api.nytimes.com/svc/search/v2/

   GNEWS_API_KEY=your_gnews_api_key
   GNEWS_BASE_URL=https://gnews.io/api/v4/
   ```

## 🐍 Running the Project  
1. Ensure the virtual environment is activated.  
2. Run the application using Streamlit:  
   ```sh
   streamlit run main.py
   ```

## 🧪 Running the Test Suite  
1. Ensure the virtual environment is activated.  
2. Run the tests:  
   ```sh
   python run_tests.py
   ```
