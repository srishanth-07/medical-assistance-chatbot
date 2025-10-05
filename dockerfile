FROM python:3.10-slim-buster

WORKDIR /app

COPY . /app
COPY data/Medical_book.pdf /app/data/Medical_book.pdf

RUN pip install -r requirements.txt

CMD ["python3", "app.py"]