from flask import Flask, render_template, Response, jsonify
import cv2, threading, time
from datetime import datetime
from tracker_core import process_frame, tracker_cam1, tracker_cam2, SRC1, SRC2, match_logs

app = Flask(__name__)

cap1 = cv2.VideoCapture(SRC1)
cap2 = cv2.VideoCapture(SRC2)
frame_cam1, frame_cam2 = None, None

# Statistics tracking
start_time = time.time()
detection_stats = {
    'total_detections': 0,
    'active_tracks': 0,
    'cam1_detections': 0,
    'cam2_detections': 0,
    'alerts_today': 0
}

def run_camera(cam_id, cap, tracker):
    global frame_cam1, frame_cam2
    while True:
        ret, frame = cap.read()
        if not ret: break
        processed = process_frame(frame, tracker, cam_id)
        _, jpeg = cv2.imencode('.jpg', processed)
        if cam_id == 1:
            frame_cam1 = jpeg.tobytes()
        else:
            frame_cam2 = jpeg.tobytes()

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames(camera=1):
    global frame_cam1, frame_cam2
    while True:
        frame = frame_cam1 if camera == 1 else frame_cam2
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed/<int:camera>')
def video_feed(camera):
    return Response(gen_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/stats')
def get_stats():
    """API endpoint to get real-time statistics"""
    global detection_stats, start_time
    
    # Calculate uptime
    uptime_seconds = int(time.time() - start_time)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    uptime = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    # Update detection counts from match_logs
    detection_stats['total_detections'] = len(match_logs)
    detection_stats['alerts_today'] = len([log for log in match_logs 
                                         if log.get('time', '').startswith(datetime.now().strftime('%Y-%m-%d'))])
    
    return jsonify({
        'total_detections': detection_stats['total_detections'],
        'active_tracks': detection_stats['active_tracks'],
        'cam1_detections': detection_stats['cam1_detections'],
        'cam2_detections': detection_stats['cam2_detections'],
        'alerts_today': detection_stats['alerts_today'],
        'uptime': uptime,
        'system_status': 'online',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/camera/<int:camera>/info')
def get_camera_info(camera):
    """API endpoint to get camera-specific information"""
    cap = cap1 if camera == 1 else cap2
    
    # Get camera properties
    fps = cap.get(cv2.CAP_PROP_FPS) if cap.isOpened() else 0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) if cap.isOpened() else 0
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) if cap.isOpened() else 0
    
    return jsonify({
        'camera_id': camera,
        'fps': int(fps) if fps > 0 else 30,
        'resolution': f"{width}x{height}" if width > 0 and height > 0 else "1920x1080",
        'status': 'online' if cap.isOpened() else 'offline',
        'detections': detection_stats.get(f'cam{camera}_detections', 0)
    })

@app.route('/api/alerts')
def get_alerts():
    """API endpoint to get recent alerts"""
    recent_alerts = match_logs[-10:] if match_logs else []
    return jsonify({
        'alerts': recent_alerts,
        'count': len(recent_alerts)
    })

if __name__ == '__main__':
    t1 = threading.Thread(target=run_camera, args=(1, cap1, tracker_cam1))
    t2 = threading.Thread(target=run_camera, args=(2, cap2, tracker_cam2))
    t1.daemon = True; t2.daemon = True
    t1.start(); t2.start()
    app.run(host='0.0.0.0', port=5000, debug=False)
