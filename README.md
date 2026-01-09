# ToDo FastAPI API

A REST API boilerplate for a ToDo application built with Python and FastAPI. This project provides a solid foundation for building a feature-rich task management service.

## Features

- **User Authentication**: Secure registration and login using JWT (JSON Web Tokens) and bcrypt password hashing.
- **Task Management**: Full CRUD operations for tasks.
  - **Create**: Add new tasks with titles and descriptions.
  - **Read**: specific task retrieval or list all user tasks.
  - **Update**: Modify task details.
  - **Delete**: Remove tasks.
- **Ownership Isolation**: Users can only access and modify their own tasks.
- **User Profile**: Endpoint to retrieve current user details, including an optional phone number.
- **Containerized**: Runs in a Docker container for consistent development and deployment.
- **Database Migrations**: Alembic integration for managing database schema changes.
- **Async Database**: High-performance asynchronous database interactions with PostgreSQL.
- **Automated Testing**: Comprehensive test suite with `pytest`, covering auth, tasks, and user flows on an isolated test database.
- **Health Check**: Monitoring endpoint to verify service status.
- **Modular Architecture**: Scalable, organized codebase separating concerns (schemas, endpoints, crud, models).

## Project Structure

```text
├── .env
├── .dockerignore
├── .gitignore
├── .venv/
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
├── README.md
├── requirements-dev.txt
├── requirements.txt
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── router.py
│   │       └── endpoints/
│   │           ├── auth.py
│   │           ├── db_ping.py
│   │           ├── health.py
│   │           ├── tasks.py
│   │           └── users.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   └── schemas/
│       ├── task.py
│       ├── token.py
│       └── user.py
├── alembic/
│   ├── versions/
│   └── env.py
└── tests/
    ├── conftest.py
    ├── test_auth.py
    ├── test_tasks.py
    └── test_users.py
```

## Database

This project is set up to use **SQLAlchemy** with an **asyncpg** driver for asynchronous interaction with a **PostgreSQL** database.

- **Configuration**: The database connection is managed in `app/core/config.py` in `app/db/session.py`.
- **Testing**: Uses a separate PostgreSQL database (`todo_test_db`) to ensure data isolation.

### Database Migrations

This project uses **Alembic** to handle database migrations.

- **Creating a New Migration**:
  When you make changes to the SQLAlchemy models (e.g., adding a column), generate a new migration script:
  ```bash
  alembic revision --autogenerate -m "A short description of the changes"
  ```

- **Applying Migrations**:
  To apply all pending migrations to the database, run:
  ```bash
  alembic upgrade head
  ```

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
- Python 3.9+

### Installation

1.  **Clone the repository (optional)**
    If you have this project in a git repository, clone it first. Otherwise, just navigate to your project directory.

2.  **Create and Activate a Virtual Environment**
    It's highly recommended to use a virtual environment to manage project dependencies.

    -   **On Windows:**
        ```powershell
        # Create the virtual environment
        python -m venv .venv

        # Activate the virtual environment
        .\.venv\Scripts\Activate.ps1
        ```
        > **Note:** If you encounter an `UnauthorizedAccess` error in PowerShell, you may need to change the execution policy for the current process. Run the following command and then try activating the environment again:
        > ```powershell
        > Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
        > ```

    -   **On macOS / Linux:**
        ```bash
        # Create the virtual environment
        python3 -m venv .venv

        # Activate the virtual environment
        source .venv/bin/activate
        ```

3.  **Install Dependencies**
    With your virtual environment active, install the required packages.
    ```bash
    # Install runtime dependencies
    pip install -r requirements.txt
    
    # Install development dependencies (for testing)
    pip install -r requirements-dev.txt
    ```

### Running the Application

Once the dependencies are installed, you can start the development server using Uvicorn.

```bash
uvicorn app.main:app --reload
```
- The `--reload` flag makes the server automatically restart after code changes.
- The API will be running at **http://127.0.0.1:8000**.
- You can access the interactive API documentation (Swagger UI) at **http://127.0.0.1:8000/docs**.

## Running Tests

To run the automated tests for this project, ensure you have installed the development dependencies and the test database exists.

1.  **Prepare Test Database**
    Ensure the test database exists in PostgreSQL:
    ```bash
    docker-compose exec db psql -U myuser -d todo_db -c "CREATE DATABASE todo_test_db;"
    ```

2.  **Run Tests**
    Execute the following command to run the test suite with pytest:
    ```bash
    pytest
    ```
    This will execute all tests in the `tests/` directory, using the isolated test database (`todo_test_db`).

## API Endpoints

Here is a summary of the available endpoints.

### Authentication
| Method | Path | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/auth/signup` | Register a new user. |
| `POST` | `/api/v1/auth/login` | Login to get an access token. |

### Users
| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/users/me` | Get current logged-in user details. |

### Tasks
| Method | Path | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/tasks/` | Create a new task. |
| `GET` | `/api/v1/tasks/` | Get all tasks for the current user. |
| `GET` | `/api/v1/tasks/{task_id}` | Get a specific task by ID. |
| `PATCH` | `/api/v1/tasks/{task_id}` | Update a specific task. |
| `DELETE` | `/api/v1/tasks/{task_id}` | Delete a specific task. |

### Health
| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Checks if the application is running. |

### Deactivating the Environment
When you are finished working, you can deactivate the virtual environment:
```bash
deactivate
```
