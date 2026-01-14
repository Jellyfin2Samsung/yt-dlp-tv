FROM python:3.12-slim

# ffmpeg needed for merge/remux
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY server.py /app/server.py

ENV MEDIA_DIR=/media
VOLUME ["/media"]
EXPOSE 8080

CMD ["python", "/app/server.py"]
