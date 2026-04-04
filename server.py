from flask import Flask, request, Response, jsonify, send_from_directory
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Servir o frontend
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# Gerar imagem
@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json

        prompt = data.get('prompt')
        model = data.get('model')
        api_key = data.get('apiKey')

        if not prompt or not api_key:
            return jsonify({"error": "Prompt ou API Key ausente"}), 400

        response = requests.post(
            f"https://router.huggingface.co/hf-inference/models/{model}",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "inputs": prompt,
                "options": {"wait_for_model": True}
            },
            timeout=60
        )

        if response.status_code != 200:
            return jsonify({
                "error": "Erro na API",
                "details": response.text
            }), 500

        return Response(response.content, content_type='image/png')

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)