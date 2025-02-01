from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json  

app = Flask(__name__)
CORS(app)

OLLAMA_API_URL = "http://localhost:11434/api/generate"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt", "")

    response = requests.post(
        OLLAMA_API_URL,
        json={"model": "gemma:2b", "prompt": prompt, "stream": True},
        stream=True
    )

    # Process the streaming response
    full_response = ""
    try:
        for line in response.iter_lines():
            if line:
                json_line = json.loads(line)
                full_response += json_line.get("response", "")
    except json.JSONDecodeError as e:
        return jsonify({"error": "Invalid response from Ollama API", "details": str(e)}), 500

    # Return the full response to the frontend
    return jsonify({"response": full_response})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
