import cv2
from modules.img_list import ImageList
from flask import Response
from typing import Tuple

class ImageInput :
    def __init__(self, img_list: ImageList, dimensions: Tuple[int, int] = (800, 600), recon: bool =True) :
        self.img_list = img_list
        self.dimensions = dimensions
        self.cam = cv2.VideoCapture(0)

        self.recon = recon

        self.rgb_colors = {
            'devan': (255, 255, 0),
            'rahmat': (0, 252, 124),
            'dayu': (57, 0, 199),
            'leo': (139, 0, 0),
            'ndak tau saya': (0, 0, 200)
        }

        self.streaming = False 

    def stop_streaming(self) -> None :
        self.cam.release()
        self.streaming = False 
    
    def start_streaming(self) -> None :
        self.streaming = True 
        return Response(self.play_web_cam(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def play_web_cam(self) -> None :
        self.cam.open(0)
        
        while self.streaming :

            # read frame from camera
            ok, frame = self.cam.read()

            if not ok :
                print('Error: could not read frame')
                return 
            
            face_locs, names = self.img_list.detect_faces(frame)

            for face_loc, name in zip(face_locs, names) :
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

                rgb_color = self.rgb_colors[name]

                cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, rgb_color, 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), rgb_color, 4)

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
