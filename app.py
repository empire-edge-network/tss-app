from flask import Flask, request, send_file, jsonify
import edge_tts
import asyncio
import uuid
import os
import base64

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
            return jsonify({"error": "No text provided"}), 400

        voice = data.get("voice", "en-US-DavisNeural")
        output_file = f"/tmp/output_{uuid.uuid4()}.mp3"

        # Clean text
        text_clean = (
            text.replace("```", "")
                .replace("‘", "'").replace("'", "'")
                .replace("“", '"').replace("”", '"')
                .replace("*", "")
                .replace("—", "-")
                .replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
                .strip()
        )

        if len(text_clean) < 50:
            text_clean += " This extra text ensures TTS can generate audio."

        # Run Edge-TTS
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        communicate = edge_tts.Communicate(text_clean, voice)
        loop.run_until_complete(communicate.save(output_file))
        loop.close()

        # Read audio file and encode to base64
        with open(output_file, "rb") as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
        
        # Clean up
        os.remove(output_file)
        
        # Return JSON with base64 audio data
        return jsonify({
            "success": True,
            "audio_data": audio_data,
            "text_length": len(text_clean)
        })

    except Exception as e:
        return jsonify({"error": f"TTS generation failed: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
