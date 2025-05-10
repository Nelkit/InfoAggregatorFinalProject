from aggregator.app import AggregatorApp
from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":
    app = AggregatorApp()
    app.run()
