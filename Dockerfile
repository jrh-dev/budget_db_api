FROM python:3.12-slim

ADD requirements.txt .

ADD . api

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 57948

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "57948"]