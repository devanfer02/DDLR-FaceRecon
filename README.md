# Face Recognition : PSD-A Final Project

## Development Setup 
1. run command ```pip install -r requirements.txt``` to install needed library
2. run command ```npm install``` to install tailwind 
3. run command ```npm run dev``` to build tailwindcss file
3. run command ```python app.py``` to run the server

## How to Use
1. Make a base image directory to store each person's image
2. Configure the base image path in [app.py](./app.py)
3. Inside base image directory, make a directory again for each person's image and name the directory the person's name.
4. Store person's image according to its directory
5. Configure the list names in [app.py](./app.py)
6. Make sure the list names is same as the directory that was created

Here's an example of directory structure : 
```
| DDLR-FaceRecon // root
|-- app.py
|-- ...
|-- img // base image directory
|   |-- budi
|   |   |-- budi01.jpg
|   |   |-- budi02.jpg
|   |-- andi
|   |   |-- andi01.jpg
```

Configuration example in [```app.py```](./app.py)
```
img_list = ImageTrainer(
    list_names=['andi', 'budi'], 
    base_img_path='img'
)
```

## Libary Used
1. [Face Recognition](https://github.com/ageitgey/face_recognition)
2. [OpenCV](https://pypi.org/project/opencv-python/)
3. [Flask](https://flask.palletsprojects.com/en/3.0.x/)

## NOTES
1. To install face_recognition library, you need to install C++ CMake Tools first. You can follow [this instruction](https://www.youtube.com/watch?v=TC_LPpa7uj0) to install C++ CMake Tools for windows.

## Group Members

Names | NIM | 
--- | --- |
Ateyna Dzazulfa Masdarofa | 225150600111009 | 
Devan Ferrel | 225150600111031 |
Rahmat Aramadhan Husni | 225150607111008
Syeikh Arsy Leonard Jafara Al Ghouf | 225150607111013