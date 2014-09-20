import os
from flask import Flask, request, redirect, url_for, jsonify
from werkzeug import secure_filename
rmq_disabled = False
try:
    import pika
    from pika.exceptions import AMQPConnectionError
except ImportError:
    rmq_disabled = True
import atexit

if not rmq_disabled:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            'localhost'))
        atexit.register(lambda: connection.close())
        channel = connection.channel()
        channel.queue_declare('files_queue', durable = True)
    except AMQPConnectionError:
        rmq_disabled = True

if rmq_disabled:
    print 'WARN: RMQ disabled'

UPLOAD_FOLDER = os.getcwd() + '/../run/data'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if not rmq_disabled:
                channel.basic_publish(exchange='',
                        routing_key="files_queue",
                        body=filename,
                        properties=pika.BasicProperties(
                            delivery_mode = 2, # make message persistent
                        ))
            return '%s\n' % jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
