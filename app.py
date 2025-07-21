from flask import Flask, request, send_file
from moviepy.editor import *
import gdown
import os

app = Flask(__name__)

@app.route('/merge', methods=['GET'])
def merge_videos():
    chroma_id = request.args.get('chroma_id')
    background_id = request.args.get('background_id')

    chroma_path = "chroma.mp4"
    background_path = "background.mp4"

    gdown.download(f"https://drive.google.com/uc?id={chroma_id}", chroma_path, quiet=False)
    gdown.download(f"https://drive.google.com/uc?id={background_id}", background_path, quiet=False)

    chroma_clip = VideoFileClip(chroma_path).resize(height=720)
    background_clip = VideoFileClip(background_path).resize(height=720)

    if background_clip.duration < chroma_clip.duration:
        background_clip = background_clip.loop(duration=chroma_clip.duration)

    background_clip = background_clip.subclip(0, chroma_clip.duration)
    chroma_clip = chroma_clip.set_position("center")

    final_clip = CompositeVideoClip([background_clip, chroma_clip.set_opacity(1)])
    final_clip.write_videofile("output_video.mp4", codec="libx264", audio_codec="aac")

    return send_file("output_video.mp4", as_attachment=True)

if __name__ == '__main__':
    app.run()
