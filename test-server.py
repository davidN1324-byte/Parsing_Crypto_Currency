from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='docs')

DOCS_DIR = os.path.join(os.getcwd(), 'docs')

@app.route('/')
def serve_index():
    return send_from_directory(DOCS_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(DOCS_DIR, filename)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)