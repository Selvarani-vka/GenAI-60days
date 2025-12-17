import asyncio
import sounddevice as sd
import soundfile as sf
import tempfile
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

SAMPLE_RATE = 16000
SILENCE_TIMEOUT = 10  # seconds


def record_audio(seconds=4):
    print("🎧 Listening...")
    audio = sd.rec(
        int(seconds * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
    )
    sd.wait()
    return audio


def play_audio(file_path):
    data, samplerate = sf.read(file_path, dtype="float32")
    sd.play(data, samplerate)
    sd.wait()


async def speak(text: str):
    print(f"🤖 Assistant: {text}")

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text,
        )
        f.write(response.read())
        audio_path = f.name

    play_audio(audio_path)


async def listen_and_transcribe():
    audio = record_audio()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, audio, SAMPLE_RATE)

        transcript = client.audio.transcriptions.create(
            file=open(f.name, "rb"),
            model="whisper-1",
        )

    return transcript.text.strip()


async def main():
    print("🎤 Console Voice Agent started\n")

    await speak("Hello! How can I help you today?")

    sleeping = False

    while True:
        try:
            try:
                # Wait for user speech, timeout = silence
                text = await asyncio.wait_for(
                    listen_and_transcribe(),
                    timeout=SILENCE_TIMEOUT,
                )
            except asyncio.TimeoutError:
                if not sleeping:
                    sleeping = True
                    await speak("I am here for you. Talk anytime for any assistance.")
                continue

            if not text:
                continue

            print(f"👂 Heard: {text}")

            if sleeping:
                sleeping = False
                await speak("I'm back. How can I help?")

            # GPT response
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a friendly voice assistant.",
                    },
                    {"role": "user", "content": text},
                ],
            )

            reply = response.choices[0].message.content
            await speak(reply)

        except KeyboardInterrupt:
            print("\n👋 Exiting voice agent.")
            break


if __name__ == "__main__":
    try: asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Voice agent stopped cleanly.")
    except asyncio.CancelledError:
        print("\n👋 Voice agent cancelled.")