from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
from pedalboard import Pedalboard, NoiseGate, Compressor, LowShelfFilter, Gain, AudioFile
import noisereduce as nr
import speech_recognition as sr
from langdetect import detect
from google.cloud import translate_v2 as translate
from elevenlabs.client import ElevenLabs
import moviepy.editor as mp


class Downloader:
    def __init__(self):
        self.video_url = None
        self.output_path = None

    def set_video_url(self, video_url, output_path):
        self.video_url = video_url
        self.output_path = output_path

    def download_audio(self):
        if self.video_url is None:
            raise Exception("Video URL not set")

        yt = YouTube(self.video_url)
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()

        video_file_path = os.path.join(self.output_path, video_stream.default_filename)
        if not os.path.exists(video_file_path):
            video_stream.download(self.output_path)

        print(f'Downloading: {yt.title}')
        print('Download complete!')

        return self.convert_to_wav(video_file_path)

    def convert_to_wav(self, input_video):
        output_audio = os.path.splitext(input_video)[0] + ".wav"

        video_clip = VideoFileClip(input_video)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(output_audio)
        video_clip.close()
        audio_clip.close()

        return self.process_audio(output_audio)

    def process_audio(self, audio_path):
        sr_rate = 44100
        output_audio_enhanced = os.path.splitext(audio_path)[0] + "_enhanced.wav"

        with AudioFile(audio_path).resampled_to(sr_rate) as f:
            audio = f.read(f.frames)

        reduced_noise = nr.reduce_noise(y=audio, sr=sr_rate, stationary=True, prop_decrease=0.75)
        board = Pedalboard([
            NoiseGate(threshold_db=-30, ratio=1.5, release_ms=250),
            Compressor(threshold_db=-16, ratio=2.5),
            LowShelfFilter(cutoff_frequency_hz=400, gain_db=10, q=1),
            Gain(gain_db=10)
        ])

        effected = board(reduced_noise, sr_rate)

        with AudioFile(output_audio_enhanced, 'w', sr_rate, effected.shape[0]) as f:
            f.write(effected)

        print("Audio processing complete")
        return output_audio_enhanced


class AudioProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.translator = translate.Client()

    def extract_text_from_audio(self, audio_file_path):
        with sr.AudioFile(audio_file_path) as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.record(source)
            try:
                transcript = self.recognizer.recognize_google(audio)
                detected_language = detect(transcript)
                return transcript, detected_language
            except sr.UnknownValueError:
                return "Speech not understood", "unknown"

    def translate_text(self, text, target_language="ar"):
        if text:
            result = self.translator.translate(text, target_language=target_language)
            return result['translatedText']
        return "No text to translate"


class AudioGenerator:
    def __init__(self, api_key):
        self.client = ElevenLabs(api_key=api_key)

    def generate_audio(self, text, voice_name):
        voice = self.client.clone(description="Human voice.", name=voice_name)
        audio = self.client.generate(text=text, voice=voice, model="eleven_multilingual_v2")
        return audio

    def play_audio(self, audio):
        play(audio, notebook=True)


class VideoProcessor:
    def __init__(self, video_file_path):
        self.video_file_path = video_file_path

    def remove_audio(self):
        video_clip = VideoFileClip(self.video_file_path)
        video_clip = video_clip.set_audio(None)
        output_video_path = os.path.splitext(self.video_file_path)[0] + "_noaudio.mp4"
        video_clip.write_videofile(output_video_path)
        return output_video_path


class VideoEditor:
    def __init__(self, video_path_without_audio, audio_path):
        self.video_path_without_audio = video_path_without_audio
        self.audio_path = audio_path

    def edit_video(self):
        video = mp.VideoFileClip(self.video_path_without_audio)
        audio = mp.AudioFileClip(self.audio_path)
        video = video.set_audio(audio)
        output_video = os.path.splitext(self.video_path_without_audio)[0] + "_final.mp4"
        video.write_videofile(output_video)
        return output_video


# Example usage
if __name__ == "__main__":
    downloader = Downloader()
    downloader.set_video_url("https://www.youtube.com/watch?v=example_video_id", "./downloads")
    audio_file_path = downloader.download_audio()

    processor = AudioProcessor()
    transcript, detected_language = processor.extract_text_from_audio(audio_file_path)
    translated_text = processor.translate_text(transcript, "ar")  # Assuming translation to Arabic

    print(f"Original text: {transcript}")
    print(f"Translated text: {translated_text}")

    # Assuming you have the ElevenLabs API key
    audio_generator = AudioGenerator(api_key='your_elevenlabs_api_key')
    audio_content = audio_generator.generate_audio(translated_text, 'name_of_voice')
    audio_generator.play_audio(audio_content)

