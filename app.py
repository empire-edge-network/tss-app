@app.route("/tts", methods=["GET"])
def tts():
    raw_text = request.args.get("text")
    if not raw_text:
        raw_text = "Hello there!"

    voice = request.args.get("voice", "en-US-DavisNeural")

    output_file = f"output_{uuid.uuid4()}.mp3"

    try:
        # Parse JSON if necessary
        try:
            data = json.loads(raw_text)
            text = data.get("script", raw_text)
        except:
            text = raw_text

        async def _main():
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_file)
        asyncio.run(_main())
    except Exception as e:
        return f"TTS generation failed: {e}", 500

    return send_file(output_file, as_attachment=True)
