# 🎬 YouTube (Download/Stream) TV Service

A lightweight Docker service that enables YouTube playback on Samsung TVs by converting videos into TV-compatible MP4 formats. This resolves the common **YouTube Error 153** issue in Jellyfin for Samsung TV.

## 🚀 Features

- **Dual serving modes**: Download & serve or direct streaming
- **TV-optimized**: Automatically converts videos to Samsung TV-compatible MP4 format
- **Simple REST API**: Easy integration with Jellyfin and other applications
- **Docker-ready**: Quick deployment with persistent storage support

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/file` | POST | Downloads and merges video into a TV-safe MP4, served from `/media/<id>.mp4` |
| `/stream` | POST | Returns a temporary direct MP4 URL (with expiration) |
| `/health` | GET | Returns a health status  |

## 🐳 Installation (Docker)

### Quick Start
```bash
docker run -d \
  --name yt-dlp-tv \
  -p 8123:8080 \
  -v /volume1/docker/yt-dlp-media:/media \
  -e BASE_URL=http://192.168.2.195:8123 \
  --restart unless-stopped \
  ghcr.io/jellyfin2samsung/yt-dlp-tv:latest
```

### Configuration

| Parameter | Description | Example |
|-----------|-------------|---------|
| `-p 8123:8080` | Maps host port 8123 to container port 8080 | Change `8123` to your preferred port |
| `-v /volume1/docker/yt-dlp-media:/media` | Persistent storage for downloaded videos | Adjust path to your storage location |
| `-e BASE_URL` | Public URL for accessing the service | Use your server's IP and port |

## 🧪 Testing

Verify the service is working:
```bash
curl -X POST http://192.168.2.195:8123/file \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=CT2_P2DZBR0"}'
```

**Expected response**: A JSON object containing the media ID and download status.

## 🔧 Jellyfin Integration

1. Start the yt-dlp-tv service using the Docker command above
2. In **Samsung Jellyfin Installer**, navigate to the YouTube settings
3. Enter your server's IP address and port (e.g., `http://192.168.2.195:8123`)
4. YouTube trailers should now play without Error 153

## 📝 Use Case

This service is specifically designed to fix **YouTube Error 153** that occurs when playing YouTube trailers in Jellyfin on Samsung TVs. It acts as a local proxy that:
- Fetches YouTube videos using yt-dlp
- Converts them to Samsung TV-compatible formats
- Serves them locally to bypass YouTube's restrictions

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | Change the host port: `-p 8124:8080` |
| Videos not saving | Verify the volume path exists and has write permissions |
| Cannot connect | Ensure `BASE_URL` matches your server's accessible IP address |

## 📄 License

This project uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) for video downloading.

## 🔗 Related Projects

- [Samsung Jellyfin Installer](https://github.com/PatrickSt1991/Samsung-Jellyfin-Installer) - Install Jellyfin on Samsung TVs
- [Jellyfin](https://jellyfin.org/) - Free media server solution
