# 1. Base Image: Start with a lightweight version of Python
FROM python:3.10-slim

# 2. Environment Variables:
# - PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files
# - PYTHONUNBUFFERED: Ensures logs are streamed directly to the console
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Work Directory: Create a folder inside the container and work there
WORKDIR /app

# 4. Dependencies: Copy just the requirements file first
# (This is a caching trick - if requirements don't change, Docker skips this step next time!)
COPY requirements.txt .

# 5. Install: Run pip inside the container
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy Code: Copy the rest of your application code into the container
COPY . .

# 7. Command: The command to run when the container starts
# We use 0.0.0.0 to make it accessible outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]