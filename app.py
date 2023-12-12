from flask import Flask, Response, render_template
import cv2 
from img_list import ImageList

app = Flask(__name__)
cam = cv2.VideoCapture(0)
img_list = ImageList(['devan','dayu','leo','rahmat'], 'img')

def generate_frames() :
    while True :

        # read frame from camera
        ok, frame = cam.read()

        if not ok :
            print('Error: could not read frame')
            return 
        
        face_locs, names = img_list.detect_faces(frame)

        for face_loc, name in zip(face_locs, names) :
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,0), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index() :
    return render_template('index.html')

@app.route('/video')
def video() :
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	app.run(debug=True, port=5600)

