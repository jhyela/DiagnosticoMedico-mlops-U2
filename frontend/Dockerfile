FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt

COPY main.py main.py

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "main.py"]