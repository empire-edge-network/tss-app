from flask import Flask, request, send_file
import edge_tts
import asyncio
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    return "TTS API is running! Use /tts?text=YOUR_TEXT to generate voice."

@app.route("/tts", methods=["GET"])
def tts():
    # Get text from query parameter
    text = request.args.get("text", "Hello there!")
    # Default male voice
    voice = request.args.get("voice", "en-US-DavisNeural")

    # Create a unique filename per request to avoid conflicts
    output_file = f"output_{uuid.uuid4()}.mp3"

    # Async function to generate TTS
    async def _main():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)

    # Run the async function
    asyncio.run(_main())

    # Send the generated MP3 file as a download
    return send_file(output_file, as_attachment=True)

# Run Flask app (Render will handle the server)
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render provides PORT env variable
    app.run(host="0.0.0.0", port=port)

