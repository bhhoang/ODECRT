import easyocr
import cv2
import numpy as np
from flask import Flask, request, jsonify
import shutil

# Path: main.py
def get_text(img):
    reader = easyocr.Reader(['en'], gpu=True)
    result = reader.readtext(img)
    return result

def get_text_only(img):
    reader = easyocr.Reader(['en'], gpu=True)
    result = reader.readtext(img)
    text = ""
    for i in range(len(result)):
        text += result[i][1] + " "
    return text

app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    return (
        "<h1>API is working</h1>"
        "<p>Upload an image to get text from it</p>"
        '<form method="post" enctype="multipart/form-data" action="/upload">'
        '<input type="file" name="file">'
        '<input type="submit">'
        "</form>"
    )

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        # Save the file to ./uploads
        f.save(f.filename)
        # Make prediction
        img = cv2.imread(f.filename)
        result = get_text_only(img)
        if not result:
            return jsonify({"result": "No text found"}), 200, {'ContentType': 'application/json'}
        return jsonify({"result": result}), 200, {'ContentType': 'application/json'}
        # Remove the image
        shutil.rmtree(f'./{f.filename}')
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)