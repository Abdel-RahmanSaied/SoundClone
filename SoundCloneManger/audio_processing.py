# from googletrans import Translator
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import moviepy.editor as mp
import speech_recognition as sr
from langdetect import detect

from translate import Translator


class AudioProcessor:
    def __init__(self):
        self.translator = Translator(from_lang='english', to_lang='arabic')
        self.recognizer = sr.Recognizer()

    def get_audio_from_video(self):
        pass

    def run(self, audio_file_path, src='english', dest='arabic'):
        original_text, original_lang = self.extract_text_from_audio(audio_file_path)
        input = original_text
        translated_text = self.translator.translate("How are you fucken boy")
        print("Translated text:", translated_text)
        return translated_text
        # return translated_text.text

    def extract_text_from_audio(self, audio_file_path, inactivity_timeout=360):
        recognizer = self.recognizer

        with sr.AudioFile(audio_file_path) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source, duration=None)  # Record the entire audio file

            try:
                # Use Google Web Speech API to recognize the speech
                transcript = recognizer.recognize_whisper(audio)
                detected_language = detect(transcript)

                print("Text extracted from audio:\n", transcript)
                print("Detected language:", detected_language)

                return transcript, detected_language

            except Exception as e:
                print("Error occurred:", e)
                raise e

    def translate_text(self, text, source_language, target_language):
        translator = self.translator

        try:
            translation = translator.translate(text, src=source_language, dest=target_language)
            print("Translation: \n", translation.text)
            return translation.text

        except Exception as e:
            raise e


class AudioGenerator:
    def __init__(self, audio_file_path):
        self.client = ElevenLabs(api_key='4cfaf4f055b3677247d47f2766a2a7c0')
        self.audio_file_path = audio_file_path
        self.translated_text = None

    def generate_audio(self, name, translated_text):
        # Upload the enhanced audio file
        voice = self.client.clone(
            description="Human voice.",
            name="name",
            files=[self.audio_file_path]
        )

        # Generate audio
        audio = self.client.generate(
            text=translated_text,
            voice=voice,
            model="eleven_multilingual_v2"
        )

        return audio

    def play_audio(self, audio):
        # Play audio
        play(audio, notebook=True)
