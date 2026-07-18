from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import analysis

app = Flask(__name__, static_folder='static')
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
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True, port=5005)
