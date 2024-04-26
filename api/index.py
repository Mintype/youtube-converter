from flask import Flask, render_template, request, send_file, after_this_request
from pytube import YouTube
import os 

current_directory = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/faq', methods=['GET'])
def faq():
    return render_template('faq.html')

@app.route('/api', methods=['POST'])
def api():
    url = request.form['url']
    try:
        video = YouTube(url)
        stream = video.streams.filter(only_audio=True).first()
        audio_path = os.path.join(current_directory, '..', f"{video.title}.mp3")
        stream.download(filename=audio_path)
        print("The video is downloaded in MP3")
        if os.path.exists(audio_path):
            @after_this_request
            def remove_file(response):
                os.remove(audio_path)
                return response
            return send_file(audio_path, as_attachment=True)
        else:
            return 'Error: File not found.'
    except Exception as e:
        print(f"Error: {e}")
        return 'Error occurred while processing the video.'

if __name__ == '__main__':
    app.run()