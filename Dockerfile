FROM python:3.12-slim

WORKDIR /api

ADD requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ADD . .

EXPOSE 57948

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "57948"]