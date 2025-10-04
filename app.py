from flask import Flask, request, send_file
import edge_tts
import asyncio
import uuid
import os
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "TTS API is live! Use POST /tts with JSON {'text': '...', 'voice': 'en-US-DavisNeural'}"

@app.route("/tts", methods=["POST"])
def tts():
    try:
        data = request.get_json(force=True)
        text = data.get("text", "").strip()
        if not text:
            return "Error: No text provided", 400

        voice = data.get("voice", "en-US-DavisNeural")
        output_file = f"output_{uuid.uuid4()}.mp3"

        # Properly create a new event loop for Edge-TTS
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        communicate = edge_tts.Communicate(text, voice)
        loop.run_until_complete(communicate.save(output_file))
        loop.close()

        return send_file(output_file, as_attachment=True)
    except Exception as e:
        return f"TTS generation failed: {e}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
