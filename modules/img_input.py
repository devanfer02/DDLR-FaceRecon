import cv2
from modules.img_trainer import ImageTrainer
from flask import Response
from typing import Tuple
import numpy as np 

class ImageInput :
    def __init__(self, img_trainer: ImageTrainer, dimensions: Tuple[int, int] = (800, 600), recon: bool =True) :
        self.img_trainer = img_trainer
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
        self.streaming = False 
        self.cam.release()
    
    def start_streaming(self, option: int = 1) -> None :
        self.streaming = True 

        if option == 1 :
            return Response(self.webcam_recognize(), mimetype='multipart/x-mixed-replace; boundary=frame')
        else :
            return Response(self.play_webcam(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    def __recognize(self, img) :
        face_locs, names = self.img_trainer.detect_faces(img)

        for face_loc, name in zip(face_locs, names) :
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            rgb_color = self.rgb_colors[name]

            cv2.putText(img, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, fontScale=1.2, color=rgb_color, thickness=1)
            cv2.rectangle(img, (x1, y1), (x2, y2), rgb_color, 4)

        return img
    
    def recognize_taken_image(self) -> Response :
        ok, frame = self.cam.read()

        self.stop_streaming()

        if not ok :
            print('ERR: cant read frame')
            return 

        frame = cv2.flip(frame, 1)
        frame = self.__recognize(frame)

        _, buffer = cv2.imencode('.jpg', frame)
        img_str = buffer.tobytes()

        return Response(img_str, mimetype='image/jpeg')

    def recognize_uploaded_image(self, image) -> Response :
        img_data = image.read()
        img_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

        processed_img = self.__recognize(img)
        _, buffer = cv2.imencode('.jpg', processed_img)
        img_str = buffer.tobytes()

        return Response(img_str, mimetype='image/jpeg')

    def play_webcam(self) -> None :
        self.cam.open(0)
        
        while self.streaming :
            ok, frame = self.cam.read()
            
            if not ok :
                print('Error: could not read frame')
                break

            frame = cv2.flip(frame, 1)
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def webcam_recognize(self) -> None :
        self.cam.open(0)
        
        while self.streaming :

            # read frame from camera
            ok, frame = self.cam.read()

            if not ok :
                print('Error: could not read frame')
                return 
            
            frame = cv2.flip(frame, 1)
            frame = self.__recognize(frame)

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
