FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
COPY main.py main.py
COPY model/ model/

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

#CMD ["uvicorn", "main:app","--reload","--host","0.0.0.0","--port","8000"]

CMD ["python", "main.py"]