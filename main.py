from flask import Flask, render_template, request, jsonify
from pytube import YouTube

app = Flask(__name__)


def estimate_file_size(duration, bitrate_kbps=8000):
    duration_seconds = int(duration)
    file_size_bytes = bitrate_kbps * duration_seconds * 1000 / 8
    file_size_mb = file_size_bytes / (1024 * 1024)
    return file_size_mb


def format_file_size(file_size_mb):
    return f"{file_size_mb:.2f}"


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    video_url = data.get('video_url', '')

    try:
        yt = YouTube(video_url)
        response = {
            'thumbnail_url': yt.thumbnail_url,
            'title': yt.title,
            'file_size_mb': format_file_size(estimate_file_size(yt.length))
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
