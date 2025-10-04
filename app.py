from flask import Flask, request, send_file
import edge_tts
import asyncio

app = Flask(__name__)

@app.route("/tts")
def tts():
    text = request.args.get("text", "")
    voice = "en-US-GuyNeural"
    path = "output.mp3"

    async def generate():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(path)

    asyncio.run(generate())
    return send_file(path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

