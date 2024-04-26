from pytube import YouTube
import os
from moviepy.editor import VideoFileClip

from pedalboard.io import AudioFile
from pedalboard import *

import noisereduce as nr


class DOWNLOADER:
    def __init__(self):
        self.video_url = None
        self.output_path = None

    def set_video_url(self, video_url, output_path):
        self.video_url = video_url
        self.output_path = output_path

    def download_audio(self):
        if self.video_url is None:
            raise Exception("Video URL not set")
        try:
            # Create a YouTube object
            yt = YouTube(self.video_url)

            # Get the audio stream with the highest quality
            # audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
            video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()

            # Download the audio stream
            print(f'Downloading: {yt.title}')
            video_file_path = os.path.join(os.getcwd(), "media", "videos", video_stream.default_filename)
            if not os.path.exists(video_file_path):
                video_stream.download(self.output_path)
                print('Download complete!')
            else:
                print('File already exists!')

            # video_file_path = os.path.join(os.getcwd(), video_stream.default_filename)

            print(video_file_path)

            # Define the output path for the unprocessed audio file
            # output_audio_notEnhanced = os.path.join(self.output_path, 'audio_notEnhanced.wav')

            # audio_file = self.convert_to_wav(video_file_path, output_audio_notEnhanced)

            audio_file = self.convert_to_wav(video_file_path)

            return audio_file

        except Exception as e:
            raise f'An error occurred: {e}'

    def convert_to_wav(self, input_video):
        # check if exists
        if not os.path.exists(input_video):
            raise Exception("File does not exist")

        filename = input_video.split(".")[0]
        input_video = input_video
        output_audio = f"{filename}.wav"

        # Load the video clip
        video_clip = VideoFileClip(input_video)

        # Extract audio from the video clip
        audio_clip = video_clip.audio

        # Write the audio clip to a WAV file
        audio_clip.write_audiofile(output_audio)

        # Close the video and audio clips
        video_clip.close()
        audio_clip.close()

        #return output_audio
        sr = 44100
        output_audio_enhanced = "enhancedaudio.wav"
        # Read the input audio file
        with AudioFile(output_audio).resampled_to(sr) as f:
            audio = f.read(f.frames)

        # Reduce noise
        reduced_noise = nr.reduce_noise(y=audio, sr=sr, stationary=True, prop_decrease=0.75)

        # Define pedalboard effects
        board = Pedalboard([
            NoiseGate(threshold_db=-30, ratio=1.5, release_ms=250),
            Compressor(threshold_db=-16, ratio=2.5),
            LowShelfFilter(cutoff_frequency_hz=400, gain_db=10, q=1),
            Gain(gain_db=10)
        ])

        # Apply effects to the audio
        effected = board(reduced_noise, sr)

        # Write the processed audio to a file
        with AudioFile(output_audio_enhanced, 'w', sr, effected.shape[0]) as f:
            f.write(effected)

        print("Done process_audio")
        return output_audio_enhanced

    def download_video(self):
        if self.video_url is None:
            raise Exception("Video URL not set")
        try:
            # Create a YouTube object
            yt = YouTube(self.video_url)

            # Get the audio stream with the highest quality
            # audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
            video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()

            # Download the audio stream
            print(f'Downloading: {yt.title}')
            video_stream.download(self.output_path)
            print('Download complete!')

            video_file_path = os.path.join(self.output_path, video_stream.default_filename)

            return video_file_path

        except Exception as e:
            raise f'An error occurred: {e}'
