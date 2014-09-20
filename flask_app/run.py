import os
from flask import Flask, request, redirect, url_for, jsonify
from werkzeug import secure_filename
import pika
import atexit

connection = pika.BlockingConnection(pika.ConnectionParameters(
                   'localhost'))
atexit.register(lambda: connection.close())
channel = connection.channel()
channel.queue_declare('files_queue', durable = True)

UPLOAD_FOLDER = os.getcwd() + '/../run/data'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            channel.basic_publish(exchange='',
                    routing_key="files_queue",
                    body=filename,
                    properties=pika.BasicProperties(
                        delivery_mode = 2, # make message persistent
                    ))
            return '%s\n' % jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
