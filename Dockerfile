FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim
LABEL authors="alessiodelriccio"

WORKDIR /app

RUN apt-get update &&\
    apt-get install -y --no-install-recommends libpq-dev build-essential curl &&\
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt ./

RUN pip --no-cache-dir install --upgrade pip && \
  pip --no-cache-dir install -r requirements.txt

COPY . .

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]