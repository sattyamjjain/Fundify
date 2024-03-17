FROM python:3.11-slim

WORKDIR /usr/src/app

COPY . .

RUN apt-get update && apt-get install git -y && apt-get install curl -y

RUN curl -fsSL https://ollama.com/install.sh | sh

RUN pip install --no-cache-dir -r subscriber-requirements.txt

CMD ["python", "./run_subscriber.py"]
