import cv2
import os
import face_recognition as fcr
import numpy as np
import joblib
from typing import List
from typing import Tuple

class ImageList :
    def __init__(self, list_names: List[str], base_path: str) -> None: 
        # constructor
        self.image_map = {}
        self.known_encoded = []
        self.known_names = []
        self.base_path = base_path.rstrip('/')
        self.list_names = list_names
        self.total_images = 0
        self.model_filename = 'data/face_data.joblib'

        self.__start_encode()
        
    def __start_encode(self) -> None :
        if os.path.exists(self.model_filename) :
            self.__use_existing()            

            return 

        print('Start encoding images')        
        for name in self.list_names : 
            self.__encode_person_image(name)
        
        self.__save_data()
        

    def __get_all_img(self, person_name: str) -> List[str] :
        file_names = [
            f'{self.base_path}/{person_name}/{file_name}' 
            for file_name in os.listdir(f'{self.base_path}/{person_name}/')
        ]
        return file_names

    def __save_data(self) : 
        known_data = {
            'encodings': self.known_encoded,
            'names': self.known_names
        }
        joblib.dump(known_data, self.model_filename)

    def __use_existing(self) :
        print('Using existing encoding data')
            
        loaded_known_data = joblib.load(self.model_filename)
        self.known_encoded = loaded_known_data['encodings']
        self.known_names = loaded_known_data['names']

        names_new = [name for name in self.list_names if name not in self.known_names]

        if len(names_new) != 0 :
            print(f'Detected {len(names_new)} new names')

        for name in names_new : 
            self.__encode_person_image(name)

        if len(names_new) != 0 :
            self.__save_data()
        

    def __encode_person_image(self, name) :
        print(f'Encoding {name} images in process')
        
        person_images = self.__get_all_img(name)

        if len(person_images) == 0 :
            print(f'{name} has no images')
            return 

        for img_path in person_images :
            img = cv2.imread(img_path)

            # need to convert color since opencv use bgr and face_recognition use rgb
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            face_encodings = fcr.face_encodings(rgb_img)
            
            if len(face_encodings) == 0 :
                print(f'No face detected in image file: {img_path}')
                continue
            
            img_encoded = face_encodings[0]

            self.known_encoded.append(img_encoded)
            self.known_names.append(name)

        print(f'Encoding {name} images done')
    
    def detect_faces(self, frame) -> Tuple[int, List[str]] :
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        # find all face and face encodings in the current frame
        rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = fcr.face_locations(rgb_small)
        face_encodings = fcr.face_encodings(rgb_small, face_locations, model='cnn')

        face_names = []
        for face_encoding in face_encodings :
            matches = fcr.compare_faces(self.known_encoded, face_encoding)
            name = 'ndak tau saya'

            # if match was found, use the first one
            if True in matches :
                match_index = matches.index(True)
                name = self.known_names[match_index]

            face_distances = fcr.face_distance(self.known_encoded, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index] :
                name = self.known_names[match_index]

            face_names.append(name)

        face_locations = np.array(face_locations)
        face_locations = face_locations / 0.25
        return face_locations.astype(int), face_names
