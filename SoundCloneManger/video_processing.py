import os
from pedalboard.io import AudioFile
from pedalboard import *
from langdetect import detect
from pydub import AudioSegment
import math
from moviepy.editor import VideoFileClip

import moviepy.editor as mp


class VideoProcessor:
    def __init__(self, video_file_path):
        self.video_file_path = video_file_path

    def remove_audio(self):
        # Load video file
        video_clip = VideoFileClip(self.video_file_path)

        # Extract audio
        audio = video_clip.audio

        # Convert to PyDub AudioSegment for processing
        audio_segment = AudioSegment.from_file(self.video_file_path, format="mp4")

        # Apply audio processing (replace this with your specific algorithm)
        # For example, you can apply a low-pass or high-pass filter to remove certain frequencies
        # processed_audio_segment = apply_audio_processing(audio_segment)

        # Alternatively, you can just mute the audio
        processed_audio_segment = audio_segment - 60

        # Replace original audio with processed audio
        video_clip = video_clip.set_audio(processed_audio_segment)

        # Write output video file
        video_path_without_audio = "output_video1.mp4"
        video_clip.write_videofile(video_path_without_audio, audio=audio)
        return video_path_without_audio


class VideoEditor:
    def __init__(self, video_path_without_audio, audio):
        self.video_path_without_audio = video_path_without_audio
        self.audio = audio

    def edit_video(self):

        print("Audio duration:", self.audio)

        # video = mp.VideoFileClip(self.video_path_without_audio).subclip(0, 60)
        video = mp.VideoFileClip(self.video_path_without_audio).subclip(0, 29)
        audio = mp.AudioFileClip(self.audio).subclip(0, 29)


        new_audio = mp.CompositeAudioClip([audio])
        # video.audio = new_audio
        video.audio = new_audio
        output_video = "outputVideo.mp4"
        video.write_videofile(output_video)
        return output_video
