from flask import render_template, request, jsonify
from modules.img_input import ImageInput

def setup_routes(app, img_input: ImageInput) :
    
    @app.route('/', endpoint='home')
    def index() :
        img_input.stop_streaming()
        return render_template('index.html')

    @app.route('/demo', endpoint='demo') 
    def demo() :
        img_input.stop_streaming()
        return render_template('demo.html')

    @app.route('/video')
    def video() :
        return img_input.start_streaming(1)
    
    @app.route('/cam')
    def cam() :
        return img_input.start_streaming(2)

    @app.route('/stopcam', methods=['POST'])
    def stop_cam() :
        img_input.stop_streaming()
        return jsonify({
            'message' : 'successfully stop video'
        })

    @app.route('/recognize', methods=['POST'])
    def recognize() :
        uploaded_file = request.files['file']

        if uploaded_file.filename == '' :
            return jsonify({
                'error': 'no file uplaoded'
            })

        return img_input.recognize_uploaded_image(uploaded_file)

    @app.route('/takeimg', methods=['POST'])
    def take_img() :
        return img_input.recognize_taken_image()
        