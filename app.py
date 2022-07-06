import os
from flask import Flask, render_template, request, session,redirect, url_for, send_file
from numpy import save
from werkzeug.utils import secure_filename
import PyPDF2

app = Flask(__name__, static_folder='static', template_folder='templates')
UPLOAD_FOLDER = os.path.join(os.getcwd(),'upload') 

def open_file(file):
    if file:
        read_pdf = PyPDF2.PdfFileReader(file)
        page = read_pdf.getPage(0)
        page_content = page.extractText()
        return page_content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['pdf']
    savePath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(savePath)    
    print(savePath)
    
    texto = open_file(savePath)
    return render_template('index.html',text = texto)
    #return 'Upload com sucesso'

@app.route('/get-file/<filename>')
def getFile(filename):
    file = os.path.join(UPLOAD_FOLDER, filename+'.png')
    return send_file(file, mimetype="image/png")

if __name__ == '__main__':
    app.run(debug=True, port=3000)