FROM python:3.10-slim-buster

WORKDIR /app

# Copy only requirements first to use Docker layer caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the app
COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=8080
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
