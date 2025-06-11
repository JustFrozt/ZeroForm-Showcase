# run.py

from app import create_app
from dotenv import load_dotenv

# This loads the standard .env file by default.
# It's used when you run `python run.py` for local development.
load_dotenv()

# The if __name__ == "__main__" block is crucial.
# It ensures that this code only runs when you execute `python run.py` directly.
# It does NOT run when Gunicorn imports the app in the Docker container.
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)