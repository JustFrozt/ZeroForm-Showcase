# Flask Notes API (Production Ready)

This is a production-ready REST API for creating and managing notes. It is delivered as a fully containerized application using Docker for easy and reliable deployment.

## Features

-   **User Authentication:** Secure user registration and JWT-based authentication.
-   **CRUD Operations:** Full Create, Read, Update, and Delete functionality for notes.
-   **Secure & Private:** Each user can only access their own notes.
-   **Containerized:** Packaged with Docker and Docker Compose for one-command startup.
-   **Production-Grade:** Served with a Gunicorn WSGI server and backed by a PostgreSQL database.
-   **Maintainable:** Uses Flask-Migrate to handle database schema changes without data loss.
-   **API Documentation:** Live, interactive API documentation via Swagger UI.
-   **Secure:** Includes rate limiting to protect against brute-force attacks.
-   **Tested:** Comes with a full suite of automated tests using Pytest.

---

## Prerequisites

To run this application, you will need:
-   Docker
-   Docker Compose

---

## How to Run the Application

### 1. Configure the Environment

First, create your own environment configuration file by copying the example:

```bash
cp .env.example .env
```

Now, open the `.env` file and change the secret keys to your own secure, random values.

### 2. Build and Run the Application

From the project's root directory, run the following command. This will build the Docker images and start the API and database containers.

```bash
docker compose up --build
```

The API will now be running and accessible at `http://localhost:8000`.

### 3. Initialize the Database (First Time Only)

The very first time you start the application, the database will be empty. You need to create the necessary tables by running the database migrations.

**Open a new, separate terminal window** (while the application is still running) and execute this command:

```bash
docker compose exec api flask db upgrade
```

Your application is now fully set up and ready to use.

---

## API Documentation

Once the application is running, you can view the interactive API documentation by navigating to the following URL in your browser:

**[http://localhost:8000/apidocs/](http://localhost:8000/apidocs/)**

From the documentation, you can explore and test all available API endpoints.

---

## Development and Maintenance

### Running Tests

To run the automated test suite, you will need a local Python environment.

1.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run pytest:**
    ```bash
    pytest -v
    ```

### Creating New Database Migrations

If you make changes to the database models in `app/models.py` (e.g., adding a new column), you must generate a new migration script.

1.  **Ensure the database container is running:**
    ```bash
    docker compose up -d db
    ```
2.  **Run the `migrate` command inside a one-off container.** This connects to the running database and detects your model changes.
    ```bash
    docker compose run --rm api flask db migrate -m "A short description of your changes"
    ```
    This will create a new script file in the `migrations/versions/` directory. This file should be committed to version control.

3.  **Apply the new migration.** The next time you deploy the application, simply run the `upgrade` command to apply the new changes to the database:
    ```bash
    docker compose exec api flask db upgrade
    ```
```

---

### `.env.example` Update

You should also make sure your `.env.example` file is up-to-date so the client knows which variables to set.

**Replace the content of `.env.example` with this:**

```
# Flask App Configuration
# IMPORTANT: Change these to long, random, and secure strings!
SECRET_KEY='a_very_secret_key_for_flask_session'
JWT_SECRET_KEY='a_very_secret_jwt_key'

# --- Database Configuration ---
# This URI tells the Flask app how to connect to the PostgreSQL database
# running in the other Docker container. The hostname 'db' is the service name
# we defined in docker-compose.yml.
SQLALCHEMY_DATABASE_URI='postgresql://user:password@db:5432/mydatabase'

# --- Variables for the Docker Compose DB service ---
# These are read by docker-compose.yml to configure the PostgreSQL container itself.
# You can change these values, but make sure they match the URI above.
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=mydatabase
```
