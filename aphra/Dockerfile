FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt ./
COPY setup.py ./
COPY config.example.toml ./config.toml

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh ./

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]