
from flask import Flask, request, jsonify
import requests

from validate import validate_input
from output_scanner import scan_output

app = Flask(__name__)




OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "llama3.2:1b"


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True)

    if not data or "message" not in data:
        return jsonify({"error": "Please provide a message."}), 400

    user_message = data["message"]

    
    validation_error = validate_input(user_message)

    if validation_error:
        return jsonify({"error": validation_error}), 400

    
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": user_message,
                "stream": False
            },
            timeout=300
        )
        response.raise_for_status()

    except requests.RequestException:
        return jsonify({"error": "AI model request failed."}), 502

    result = response.json()
    model_response = result.get("response", "")

   
    safe, scanner_error = scan_output(model_response)

    if not safe:
        return jsonify({"error": scanner_error}), 400

    return jsonify({"response": model_response}), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
