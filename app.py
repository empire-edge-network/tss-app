from flask import Flask, request, send_file
import edge_tts
import asyncio
import uuid


app = Flask(__name__)

@app.route("/tts", methods=["GET"])
def tts():
    text = request.args.get("text", "Hello there!")
    voice = request.args.get("voice", "en-US-DavisNeural")

    # create a unique filename per request
    output_file = f"output_{uuid.uuid4()}.mp3"

    async def _main():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)

    asyncio.run(_main())
    return send_file(output_file, as_attachment=True)

Fix TTS route for male voice and stability



