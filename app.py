from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import io

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "YouTube Downloader API",
        "usage": "/download?url=YOUTUBE_URL",
        "example": "/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/download')
def download():
    url = request.args.get('url')
    
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400
    
    if 'youtube.com' not in url and 'youtu.be' not in url:
        return jsonify({"error": "URL must be a valid YouTube link"}), 400
    
    try:
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info['url']
            filename = f"{info['title']}.mp4"
            
            return jsonify({
                "status": "success",
                "title": info['title'],
                "download_url": video_url,
                "message": "Video ready to download"
            })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
