from flask import Flask, request, send_file
import edge_tts
import asyncio
import uuid
import os

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
        # Save in /tmp for Render compatibility
        output_file = f"/tmp/output_{uuid.uuid4()}.mp3"

        # Clean text: remove Markdown, special characters, and line breaks
        text_clean = (
            text.replace("```", "")
                .replace("‘", "'").replace("’", "'")
                .replace("“", '"').replace("”", '"')
                .replace("*", "")
                .replace("—", "-")
                .replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
                .strip()
        )

        # Ensure minimum length
        if len(text_clean) < 50:
            text_clean += " This extra text ensures TTS can generate audio."

        # Run Edge-TTS
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        communicate = edge_tts.Communicate(text_clean, voice)
        loop.run_until_complete(communicate.save(output_file))
        loop.close()

        # Send file and delete after sending
        response = send_file(output_file, as_attachment=True)
        os.remove(output_file)
        return response

    except Exception as e:
        return f"TTS generation failed: {e}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
