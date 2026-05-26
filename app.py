from flask import Flask, request, jsonify
import yt_dlp
import os
import subprocess
import tempfile

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
        # Extract video info
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            title = info.get('title', 'video')
            
            if not video_url:
                return jsonify({"error": "Could not extract video URL"}), 500
            
            # Redirect to the actual video URL for direct download
            return jsonify({
                "status": "success",
                "title": title,
                "download_url": video_url,
                "message": "Click the download_url to download the video"
            })
    
    except yt_dlp.utils.DownloadError as e:
        return jsonify({"error": f"Download error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
