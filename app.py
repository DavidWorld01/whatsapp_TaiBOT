from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/result.png')
def serve_image():
    print("Incomed Successfully!")
    image_path = os.path.join(os.getcwd(), 'result.png')
    try:
        return send_file(image_path, mimetype='image/png')
    except:
        print("Not successfull")
@app.route('/')
def hello():
    return '<h1>Hello world</h1>'
if __name__ == '__main__':
    app.run(port=5000)
