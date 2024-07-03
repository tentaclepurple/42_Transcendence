# Use the official Python image from the Docker Hub
FROM python:3.11.9

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt \
    && apt update \
    && apt install -y netcat-openbsd \
    && pip install uvicorn

RUN apt install nodejs -y && apt install npm -y \
    && npm install -g node-gyp \
    && npm install -g truffle \
    && npm install -g solc@0.8.19	

COPY init.sh /app/init.sh

RUN chmod +x init.sh

EXPOSE 8000

CMD ["sh", "/app/backend/init.sh"]
