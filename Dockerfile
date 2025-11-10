# ---- Step 1: Base Image ----
FROM python:3.10-slim

# ---- Step 2: Set working directory ----
WORKDIR /code

# ---- Step 3: Copy project files ----
COPY . /code

# ---- Step 4: Install dependencies ----
RUN pip install --no-cache-dir -r requirements.txt

# ---- Step 5: Expose port ----
EXPOSE 8000

# ---- Step 6: Run FastAPI ----
CMD ["uvicorn", "todo_app.app.main:app", "--host", "0.0.0.0", "--port", "8000"]


