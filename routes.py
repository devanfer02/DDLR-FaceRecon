from flask import render_template, Response 
from modules.img_input import ImageInput

def setup_routes(app, img_input: ImageInput) :
    @app.route('/', endpoint='home')
    def index() :
        img_input.stop_streaming()
        return render_template('index.html')

    @app.route('/webcam', endpoint='webcam')
    def webcam() :
        return render_template('webcam.html')

    @app.route('/docs', endpoint='docs') 
    def docs() :
        img_input.stop_streaming()
        return render_template('docs.html')

    @app.route('/team', endpoint='team') 
    def team() :
        img_input.stop_streaming()
        return render_template('team.html')

    @app.route('/photo', endpoint='photo') 
    def team() :
        img_input.stop_streaming()
        return render_template('photo_recon.html')

    @app.route('/video')
    def video() :
        return img_input.start_streaming()

