from app import create_app
from dotenv import load_dotenv
import os

load_dotenv()


if __name__ == "__main__":
    app = create_app(
        development=os.environ["FLASK_ENV"] == "development"
    )
    app.run(host="0.0.0.0")
