import cv2
import os
import face_recognition as fcr
import numpy as np
import joblib
import pickle
from sklearn.svm import SVC
from typing import List
from typing import Tuple

class ImageTrainer :
    def __init__(self, list_names: List[str], base_img_path: str) -> None: 
        # constructor
        self.known_encoded = []
        self.known_names = []
        self.base_img_path = base_img_path.rstrip('/')
        self.list_names = list_names
        self.total_images = 0
        self.model_filename = 'data/face_data.sav'
        self.joblib_filename = 'data/face_data.joblib'
        self.model = SVC()

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
            f'{self.base_img_path}/{person_name}/{file_name}' 
            for file_name in os.listdir(f'{self.base_img_path}/{person_name}/')
        ]
        return file_names

    def __save_data(self) : 
        known_data = {
            'encodings': self.known_encoded,
            'names': self.known_names
        }

        self.model.fit(known_data['encodings'], known_data['names'])

        pickle.dump(self.model, open(self.model_filename, 'wb'))
        joblib.dump(known_data, self.joblib_filename)

    def __use_existing(self) :
        print('Using existing model data')
            
        loaded_known_data = joblib.load(self.joblib_filename)
        self.model = joblib.load(self.model_filename)
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
            if img_path.lower().endswith('.heic') :
                print(f'skipping {img_path} file')
                continue

            faces = fcr.load_image_file(img_path)
            face_locations = fcr.face_locations(faces)
            face_encodings = fcr.face_encodings(faces, face_locations)
            
            if len(face_encodings) == 0 :
                print(f'No face detected in image file: {img_path}')
                continue
            
            img_encoded = face_encodings[0]

            self.known_encoded.append(img_encoded)
            self.known_names.append(name)

            print(f'Encoded {img_path} image')

        print(f'Encoding {name} images done')
        print('-' * 40)
    
    def detect_faces(self, frame) -> Tuple[int, List[str]] :
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        # find all face and face encodings in the current frame
        rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = fcr.face_locations(rgb_small)
        face_encodings = fcr.face_encodings(rgb_small, face_locations)

        face_names = []
        
        for face_encoding in face_encodings :
            id_predict = self.model.predict([face_encoding])
            name = 'ndak tau saya' if len(id_predict) == 0 else id_predict[0]

            face_names.append(name)

        face_locations = np.array(face_locations)
        face_locations = face_locations / 0.25
        return face_locations.astype(int), face_names
