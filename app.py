import os
from flask import Flask, request, render_template, send_file
from moviepy.editor import VideoFileClip, CompositeVideoClip
from moviepy.video.fx.all import resize

UPLOAD_FOLDER = 'uploads'
OUTPUT_VIDEO = 'static/output.mp4'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("static", exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge_videos():
    chroma_file = request.files['chroma']
    bg_file = request.files['background']

    chroma_path = os.path.join(app.config['UPLOAD_FOLDER'], 'chroma.mp4')
    bg_path = os.path.join(app.config['UPLOAD_FOLDER'], 'background.mp4')

    chroma_file.save(chroma_path)
    bg_file.save(bg_path)

    # دمج باستخدام moviepy
    bg = VideoFileClip(bg_path)
    fg = VideoFileClip(chroma_path).resize(bg.size).set_position("center")

    fg = fg.set_duration(bg.duration)
    final = CompositeVideoClip([bg, fg])
    final.write_videofile(OUTPUT_VIDEO, codec="libx264", audio_codec="aac")

    return send_file(OUTPUT_VIDEO, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
