from flask import Flask, request, send_file
import edge_tts
import asyncio
import uuid
import os
import json

# Create Flask app
app = Flask(__name__)

# Optional home route
@app.route("/")
def home():
    return "TTS API is running! Use /tts?text=YOUR_TEXT to generate voice."

# TTS endpoint
@app.route("/tts", methods=["GET"])
def tts():
    raw_text = request.args.get("text", "Hello there!")
    voice = request.args.get("voice", "en-US-DavisNeural")
    output_file = f"output_{uuid.uuid4()}.mp3"

    # Parse Gemini JSON string safely
    try:
        data = json.loads(raw_text)
        text = data.get("script", raw_text)
    except:
        text = raw_text

    try:
        async def _main():
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_file)
        asyncio.run(_main())
    except Exception as e:
        return f"TTS generation failed: {e}", 500

    return send_file(output_file, as_attachment=True)

# Main
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
