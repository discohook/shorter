FROM python:3.8-slim

RUN apt-get update && apt-get install gcc -y

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "hypercorn", "shorter:app", "--bind", "0.0.0.0:8000", "--access-log", "-" ]
