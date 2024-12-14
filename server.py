
import os
os.system("pip install opencv-python")
os.system("pip install flask")
os.system("pip install flask_socketio")

import cv2
import base64
import time
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)

# Try setting async_mode explicitly
socketio = SocketIO(app, async_mode='threading')  # You can change 'threading' to 'eventlet' or 'gevent'

# Camera capture setup
cap = cv2.VideoCapture(0)  # Capture from the first camera


# Function to encode frames as base64 for sending to clients
def get_frame():
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # Convert frame to JPEG
        _, jpeg = cv2.imencode('.jpg', frame)

        # Convert image to base64
        jpeg_base64 = base64.b64encode(jpeg.tobytes()).decode('utf-8')

        # Emit the frame to all connected clients
        socketio.emit('video_frame', {'frame': jpeg_base64})

        # Sleep for a short period to simulate real-time frame transmission
        time.sleep(0.1)


# Function to handle client connections
@app.route('/')
def index():
    return render_template('index.html')


# Start capturing video in a separate thread
thread = threading.Thread(target=get_frame)
thread.daemon = True
thread.start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
