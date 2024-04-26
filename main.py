
from SoundCloneManger.downloader import DOWNLOADER
from SoundCloneManger.audio_processing import AudioProcessor, AudioGenerator
from SoundCloneManger.video_processing import VideoProcessor, VideoEditor

# Example usage
if __name__ == "__main__":
    translatorInstance = AudioProcessor()
    downloaderInstance = DOWNLOADER()
    downloaderInstance.set_video_url("https://www.youtube.com/watch?v=JzPfMbG1vrE", "./media/videos")
    audio_file_path = downloaderInstance.download_audio()
    translated_text = translatorInstance.run(audio_file_path)
    print(translated_text)
    text_to_speech = AudioGenerator(audio_file_path)
    audio = text_to_speech.generate_audio(translated_text=translated_text, name="name")
    print("Audio generated", audio)
    text_to_speech.play_audio(audio)
    video_file_path = "./media/videos/30 Second Explainer Videos.mp4"
    processor = VideoProcessor(video_file_path)
    video_path_without_audio = processor.remove_audio()
    print("Video with removed audio saved as:", video_path_without_audio)
    video_editor = VideoEditor(video_path_without_audio, audio)
    video_editor.edit_video()
