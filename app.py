from flask import Flask, render_template, request, send_file
import os
from moviepy.editor import VideoFileClip, CompositeVideoClip
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge():
    chroma_file = request.files['chroma']
    background_file = request.files['background']

    if not chroma_file or not background_file:
        return "الملفات غير مكتملة", 400

    chroma_path = os.path.join(UPLOAD_FOLDER, chroma_file.filename)
    background_path = os.path.join(UPLOAD_FOLDER, background_file.filename)
    
    chroma_file.save(chroma_path)
    background_file.save(background_path)

    # دمج الفيديو
    output_filename = f"merged_{uuid.uuid4().hex}.mp4"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    try:
        chroma = VideoFileClip(chroma_path).resize(height=720)
        background = VideoFileClip(background_path).resize(height=720)

        final = CompositeVideoClip([background, chroma.set_position("center")])
        final = final.set_duration(chroma.duration)
        final.write_videofile(output_path, codec='libx264', audio_codec='aac')

    except Exception as e:
        return f"حدث خطأ أثناء الدمج: {str(e)}", 500

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
