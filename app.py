from flask import Flask, request, send_file
import edge_tts
import asyncio
import uuid
import os
import json

# Create Flask app
app = Flask(__name__)

# Optional home route to confirm service is live
@app.route("/")
def home():
    return "TTS API is live! Send a POST request to /tts with JSON body {'text': 'your script', 'voice': 'voice_name'}"

# TTS endpoint
@app.route("/tts", methods=["POST"])
def tts():
    try:
        # Read JSON from POST body
        data = request.get_json(force=True)
        text = data.get("text", "").strip()
        if not text:
            return "Error: No text provided", 400

        # Voice selection (default to male professional)
        voice = data.get("voice", "en-US-DavisNeural")
        output_file = f"output_{uuid.uuid4()}.mp3"

        # Generate TTS asynchronously
        async def _main():
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_file)

        asyncio.run(_main())

        # Return generated MP3
        return send_file(output_file, as_attachment=True)

    except Exception as e:
        return f"TTS generation failed: {e}", 500

# Main entry point
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
