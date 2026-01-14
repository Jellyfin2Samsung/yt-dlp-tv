from flask import Flask, request, jsonify, send_file, abort
import subprocess
import uuid
import os
import threading
import time

MEDIA_DIR = os.environ.get("MEDIA_DIR", "/media")
BASE_URL = os.environ.get("BASE_URL", "")  # optional, e.g. http://192.168.2.195:8123
CLEANUP_SECONDS = int(os.environ.get("CLEANUP_SECONDS", "1800"))  # 30 min

os.makedirs(MEDIA_DIR, exist_ok=True)
app = Flask(__name__)

# TV-safe: prefer H264 video + M4A audio -> merged MP4
YTDLP_FMT_FILE = (
    "bv*[vcodec^=avc1][ext=mp4]+ba[ext=m4a]/"
    "bv*[vcodec=h264][ext=mp4]+ba[ext=m4a]/"
    "b[vcodec^=avc1][ext=mp4]/"
    "b[vcodec=h264][ext=mp4]"
)

# Stream mode: try to return a single progressive MP4 URL
YTDLP_FMT_STREAM = "b[vcodec^=avc1][ext=mp4]/b[vcodec=h264][ext=mp4]/b[ext=mp4]"


def _cleanup_later(path: str, delay: int):
    def _run():
        time.sleep(delay)
        try:
            os.remove(path)
        except:
            pass
    t = threading.Thread(target=_run, daemon=True)
    t.start()


def _run(cmd: list[str]) -> None:
    # Keep output for debugging; if something fails, raise
    subprocess.check_call(cmd)


@app.get("/health")
def health():
    return jsonify({"ok": True})


@app.post("/file")
def file_mode():
    data = request.get_json(silent=True) or {}
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing url"}), 400

    vid = uuid.uuid4().hex
    out = os.path.join(MEDIA_DIR, f"{vid}.mp4")

    cmd = [
        "yt-dlp",
        "--no-playlist",
        "-f", YTDLP_FMT_FILE,
        "--merge-output-format", "mp4",
        "--remux-video", "mp4",
        "-o", out,
        url,
    ]

    try:
        _run(cmd)
    except subprocess.CalledProcessError as e:
        # Clean partial
        try:
            if os.path.exists(out):
                os.remove(out)
        except:
            pass
        return jsonify({"error": "yt-dlp failed", "code": e.returncode}), 500

    _cleanup_later(out, CLEANUP_SECONDS)

    public_path = f"/media/{vid}.mp4"
    if BASE_URL:
        return jsonify({"mode": "file", "url": f"{BASE_URL}{public_path}"})
    return jsonify({"mode": "file", "url": public_path})


@app.post("/stream")
def stream_mode():
    data = request.get_json(silent=True) or {}
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing url"}), 400

    cmd = ["yt-dlp", "--no-playlist", "-f", YTDLP_FMT_STREAM, "-g", url]

    try:
        stream_url = subprocess.check_output(cmd, text=True).strip()
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "yt-dlp failed", "code": e.returncode}), 500

    if not stream_url:
        return jsonify({"error": "No stream url returned"}), 500

    return jsonify({"mode": "stream", "url": stream_url})


@app.get("/media/<path:name>")
def media(name: str):
    # only allow serving files within MEDIA_DIR
    full = os.path.join(MEDIA_DIR, name)
    if not os.path.exists(full):
        abort(404)
    return send_file(full, conditional=True)


if __name__ == "__main__":
    # Flask dev server is fine behind Docker for LAN use.
    # If you want production, we can swap to gunicorn later.
    app.run(host="0.0.0.0", port=8080)
