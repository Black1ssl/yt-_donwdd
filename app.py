from flask import Flask, request, jsonify
import yt_dlp
import os

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
        # Configure yt-dlp with better options to bypass YouTube bot detection
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'quiet': False,
            'no_warnings': False,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'socket_timeout': 30,
            'socket_local_addr': None,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            title = info.get('title', 'video')
            duration = info.get('duration', 0)
            
            if not video_url:
                return jsonify({
                    "error": "Could not extract video URL",
                    "hint": "Try a different video or check if the link is valid"
                }), 500
            
            return jsonify({
                "status": "success",
                "title": title,
                "duration": duration,
                "download_url": video_url,
                "message": "Click the download_url to download the video",
                "format": "MP4 (Best Quality)"
            })
    
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        # Check for different types of errors
        if "Sign in to confirm" in error_msg or "bot" in error_msg.lower():
            return jsonify({
                "error": "YouTube bot protection triggered",
                "hint": "Try a different video or wait a moment before retrying",
                "details": error_msg
            }), 429
        elif "Video unavailable" in error_msg or "not available" in error_msg.lower():
            return jsonify({
                "error": "Video is not available",
                "details": error_msg
            }), 400
        else:
            return jsonify({
                "error": f"Download error: {error_msg}"
            }), 400
    
    except Exception as e:
        return jsonify({
            "error": f"Unexpected error: {str(e)}",
            "type": type(e).__name__
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
