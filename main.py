from flask import Flask, render_template, request, jsonify
from pytube import YouTube
import os
import yt_dlp

app = Flask(__name__)

DOWNLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'Downloads')

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
    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400
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

@app.route('/download', methods=['POST'])
def download_video():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    try:
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
            video_ext = info_dict.get('ext', 'mp4')
            output_path = ydl.prepare_filename(info_dict)
            ydl.download([url])
            os.utime(output_path, None)
        return jsonify({'message': 'Download started', 'title': video_title, 'ext': video_ext})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
