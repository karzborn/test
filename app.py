from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
SAVE_DIR = 'downloads'

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

@app.route('/download', methods=['POST'])
def download_image():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 400

    filename = url.split('/')[-1]
    filepath = os.path.join(SAVE_DIR, filename)

    with open(filepath, 'wb') as file:
        file.write(response.content)

    return jsonify({'message': f'File saved as {filename}'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
