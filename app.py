from flask import Flask
from modules.img_list import ImageList
from modules.img_input import ImageInput
from routes.routes import setup_routes
import cv2 

app = Flask(__name__, static_url_path='/static')
cam = cv2.VideoCapture(0)
img_list = ImageList(['devan','dayu','leo', 'rahmat'], 'img')
img_input = ImageInput(img_list)

setup_routes(app, img_input)

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, port=5600, host='0.0.0.0', use_reloader=True)

