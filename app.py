from flask import Flask, request, send_file
import edge_tts
import asyncio
import uuid
import os
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "TTS API is running! Use /tts?text=YOUR_TEXT to generate voice."

@app.route("/tts", methods=["GET"])
def tts():
    raw_text = request.args.get("text", "Hello there!")

    # Safely parse if it's JSON string
    try:
        data = json.loads(raw_text)
        # If your script is nested in a JSON, take "script" key
        text = data.get("script", "Hello there!")
    except:
        text = raw_text  # if not JSON, just use raw text

    voice = request.args.get("voice", "en-US-DavisNeural")
    output_file = f"output_{uuid.uuid4()}.mp3"

    try:
        async def _main():
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_file)
        asyncio.run(_main())
    except Exception as e:
        return f"TTS generation failed: {e}", 500

    return send_file(output_file, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
