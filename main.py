from flask import Flask, render_template, request, jsonify
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    video_url = data['video_url']
    yt = YouTube(video_url)
    response = {
        'thumbnail_url': yt.thumbnail_url,
        'title': yt.title
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
