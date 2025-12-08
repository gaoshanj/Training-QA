import os
import io
import logging
import azure.functions as func

try:
    import azure.cognitiveservices.speech as speechsdk
except Exception:
    speechsdk = None

def synthesize_ssml_to_audio(ssml: str) -> bytes:
    key = os.environ.get("AZURE_SPEECH_KEY")
    region = os.environ.get("AZURE_SPEECH_REGION")
    if not speechsdk or not key or not region:
        raise RuntimeError("Speech SDK not configured. Please set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION and install azure-cognitiveservices-speech.")

    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    result = synthesizer.speak_ssml_async(ssml).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data
    else:
        raise RuntimeError(f"TTS failed: {result.reason}")

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()
    except ValueError:
        data = {}
    text = data.get("text") or data.get("ssml")
    if not text:
        return func.HttpResponse("missing text/ssml", status_code=400)
    try:
        audio = synthesize_ssml_to_audio(text)
    except Exception as e:
        logging.exception("TTS error")
        return func.HttpResponse(str(e), status_code=500)

    return func.HttpResponse(body=audio, status_code=200, mimetype="audio/mpeg")
