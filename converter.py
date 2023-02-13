from flask import Flask, request, redirect, url_for, send_from_directory
from gtts import gTTS
from PyPDF2 import PdfFileReader
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/Users/marco/Documents/python/pdftomp3withflask/archivos/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return '''
    <!doctype html>
    <html>
    <body>
    <form action="/" method="post" enctype="multipart/form-data">
    <input type="file" name="file">
    <input type="submit" value="Upload">
    </form>
    </body>
    </html>
    '''

@app.route('/', methods=['POST'])
def upload_file():
    file = request.files['file']
    print(os.path.dirname(__file__))
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        pdf_file = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb')
        pdf_reader = PdfFileReader(pdf_file)
        text = ""
        for page in range(pdf_reader.numPages):
            text += pdf_reader.getPage(page).extractText()
        tts = gTTS(text=text)
        mp3_filename = filename.split('.')[0] + ".mp3"
        tts.save(os.path.join(app.config['UPLOAD_FOLDER'], mp3_filename))
        return redirect(url_for('uploaded_file',
                                filename=mp3_filename))
    else:
        return "File not allowed"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run(debug=True)
