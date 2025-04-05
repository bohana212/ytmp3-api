from flask import Flask, request, jsonify, send_from_directory
import yt_dlp
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

@app.route('/api/ytmp3')
def download_mp3():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL tidak ada'}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")

    return jsonify({
        'title': info.get('title'),
        'thumbnail': info.get('thumbnail'),
        'mp3_url': f"/file/{os.path.basename(filename)}"
    })

@app.route('/file/<path:filename>')
def download_file(filename):
    return send_from_directory('downloads', filename)

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(host='0.0.0.0', port=5000)
