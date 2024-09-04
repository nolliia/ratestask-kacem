FROM postgres:12 as db
COPY rates.sql /docker-entrypoint-initdb.d/
ENV POSTGRES_PASSWORD=ratestask

FROM python:3.12 as app
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python3", "run.py"]