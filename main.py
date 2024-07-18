from flask import Flask, render_template, request, jsonify
from pytube import YouTube

app = Flask(__name__)


def estimate_file_size(duration, bitrate_kbps=8000):
    duration_seconds = int(duration)
    file_size_mb = bitrate_kbps * duration_seconds / 8 / 1024
    return f"{file_size_mb:.2f}"
    

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/search', methods=['POST'])
def search():
    video_url = request.get_json().get('video_url')
    try:
        yt = YouTube(video_url)
        response = {
            'thumbnail_url': yt.thumbnail_url,
            'title': yt.title,
            'file_size_mb': estimate_file_size(yt.length)
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 400



if __name__ == "__main__":
    app.run(debug=True)
