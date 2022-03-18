FROM python:3.8-slim

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-m", "hypercorn", "shorter:app", "--bind", "0.0.0.0:8000", "--access-logfile", "-" ]
