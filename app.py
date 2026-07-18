import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import analysis

# Use absolute path relative to the project root for Render deployment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, static_folder=STATIC_DIR)
CORS(app)

@app.route('/api/data', methods=['GET'])
def get_data():
    df = analysis.load_data()
    metrics = analysis.get_metrics(df)
    plot_b64 = analysis.get_plot_base64()
    raw_data = analysis.get_raw_data(df)
    
    return jsonify({
        'metrics': metrics,
        'plot': f"data:image/png;base64,{plot_b64}",
        'raw_data': raw_data
    })

@app.route('/')
def index():
    return send_from_directory(STATIC_DIR, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(STATIC_DIR, path)

if __name__ == '__main__':
    # Local development server
    app.run(debug=True, port=5005)
