## yt-dlp TV service (file + stream)

Endpoints:
- POST /file   -> downloads + merges a TV-safe MP4, served from /media/<id>.mp4
- POST /stream -> returns a temporary direct MP4 URL (expires)

### Run (Docker)
Example (host port 8123 -> container 8080):

docker run -d \
  --name yt-dlp-tv \
  -p 8123:8080 \
  -v /volume1/docker/yt-dlp-media:/media \
  -e BASE_URL=http://192.168.2.195:8123 \
  --restart unless-stopped \
  ghcr.io/<YOUR_GH_USER>/<YOUR_REPO>:latest

### Test
curl -X POST http://192.168.2.195:8123/file \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=CT2_P2DZBR0"}'
