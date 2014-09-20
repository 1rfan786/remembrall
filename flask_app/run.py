import os
from flask import Flask, request, redirect, url_for, jsonify
from werkzeug import secure_filename

UPLOAD_FOLDER = os.getcwd() + '/../run/data'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return '%s\n' % jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
