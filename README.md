# ToDo FastAPI API

A REST API boilerplate for a ToDo application built with Python and FastAPI. This project provides a solid foundation for building a feature-rich task management service.

## Features

### Completed
- **Health Check:** A `GET /api/v1/health` endpoint to verify that the service is running.
- **Modular Architecture:** Clean, scalable structure with separation of concerns.
- **Environment-based Configuration:** Using Pydantic for managing different configurations (dev, prod, test).

### To Be Implemented
- **User Authentication:** JWT-based registration and login.
- **Database Integration:** Using SQLAlchemy and aiosqlite for asynchronous database operations.
- **ToDo Management:** Full CRUD (Create, Read, Update, Delete) functionality for ToDo items.
- **File Storage:** Potential integration with a cloud storage provider like Backblaze B2.

## Database

This project is set up to use **SQLAlchemy** with an **aiosqlite** driver for asynchronous interaction with a **SQLite** database.

- **Configuration:** The database connection is managed in `app/core/config.py` and can be configured for different environments.
- **Current Status:** The necessary libraries are included in `requirements.txt`, but the database models and operational logic are not yet implemented.

## Project Analysis Summary

This project is a well-structured boilerplate, ready for the implementation of its core features. It demonstrates best practices for configuration and API design in a modern Python backend.

### Application Entrypoint (`app/main.py`)

The `main.py` file is the core of the application. It initializes the FastAPI application and brings together the other components.

*   **Middleware:** It is set up to easily add middleware for handling tasks like request correlation.
*   **Routing:** It imports and includes the main `api_router` from `app/api/v1/router.py`. This keeps the API routing organized and modular.

### Configuration (`app/core/config.py`)

The `app/core/config.py` file manages the application's configuration using Pydantic's `BaseSettings`.

*   **Environment-Based Configuration:** It defines different configuration classes for `dev`, `prod`, and `test` environments. This is a best practice for managing configuration in a real-world application.
*   **`.env` File Support:** It uses `SettingsConfigDict` to load configuration from a `.env` file. This is a standard way to manage secrets and environment-specific variables.
*   **Type-Safe Configuration:** By using Pydantic, the configuration is type-safe, providing validation and type hints for configuration variables.

### API Routes (`app/api/v1/router.py`)

The `app/api/v1/router.py` file defines the main API router.

*   **Modular Endpoints:** It is designed to include other routers from the `app/api/v1/endpoints` directory. The initial `health` endpoint is already included.
*   **Scalability:** This structure allows the API to be easily expanded with new features and versions.

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
    With your virtual environment active, install the required packages from `requirements.txt`.
    ```bash
    pip install -r requirements.txt
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

To run the automated tests for this project, you'll first need to install the development dependencies.

1.  **Install Development Dependencies**
    With your virtual environment active, install the required packages from `requirements-dev.txt`.
    ```bash
    pip install -r requirements-dev.txt
    ```

2.  **Run Tests**
    Execute the following command to run the test suite with pytest:
    ```bash
    pytest
    ```

## API Endpoints

Here is a summary of the available endpoints.

| Method | Path                | Description                                  |
|--------|---------------------|----------------------------------------------|
| `GET`  | `/api/v1/health`    | Checks if the application is running.        |

### Deactivating the Environment
When you are finished working, you can deactivate the virtual environment:
```bash
deactivate
```
