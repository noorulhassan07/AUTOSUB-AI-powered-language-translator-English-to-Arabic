from flask import Flask, render_template, Response, jsonify
from flask_socketio import SocketIO
import threading
from mic_stream import mic_stream
from translator import translation_worker
from webcam_feed import gen_frames

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start', methods=['POST'])
def start_all():
    print("🟢 mic_stream started")
    threading.Thread(target=mic_stream, daemon=True).start()
    threading.Thread(target=translation_worker, args=(socketio,), daemon=True).start()
    return jsonify({"status": "started"})



if __name__ == '__main__':
    socketio.run(app, debug=True)
