import os
import concurrent.futures
from pytube import YouTube
from moviepy.editor import AudioFileClip
import whisper
import requests
from io import BytesIO

def download_youtube_video(url):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    output_file = stream.download(filename="temp_audio.mp4")
    return output_file

def extract_audio(video_path, audio_format="mp3"):
    audio = AudioFileClip(video_path)
    audio_path = video_path.replace(".mp4", f".{audio_format}")
    audio.write_audiofile(audio_path)
    audio.close()
    os.remove(video_path)  # Remove the video after extracting audio
    return audio_path

def transcribe_audio(audio_path, model):
    result = model.transcribe(audio_path)
    return result["text"]

def process_in_parallel(audio_paths, model, max_workers=None):
    texts = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(transcribe_audio, path, model) for path in audio_paths]
        for future in concurrent.futures.as_completed(futures):
            texts.append(future.result())
    return texts

def transcribe_youtube_link(url, model, audio_format="mp3"):
    video_path = download_youtube_video(url)
    audio_path = extract_audio(video_path, audio_format)
    return transcribe_audio(audio_path, model)

def transcribe_audio_file(file_path, model):
    return transcribe_audio(file_path, model)

def split_audio(file_path, duration=600):
    audio = AudioFileClip(file_path)
    audio_splits = []
    for i in range(0, int(audio.duration), duration):
        split_path = f"{file_path}_{i}.mp3"
        split_audio = audio.subclip(i, min(i + duration, audio.duration))
        split_audio.write_audiofile(split_path)
        audio_splits.append(split_path)
    audio.close()
    return audio_splits

def main():
    model = whisper.load_model("base")
    url = input("Ingrese el enlace de YouTube o 'skip' para transcribir un archivo local: ")
    
    if url.lower() != "skip":
        transcribed_text = transcribe_youtube_link(url, model)
    else:
        file_path = input("Ingrese la ruta del archivo de audio: ")
        audio_splits = split_audio(file_path)
        transcribed_texts = process_in_parallel(audio_splits, model)
        transcribed_text = " ".join(transcribed_texts)
    
    output_file = "transcription.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(transcribed_text)
    
    print(f"Transcripción completada y guardada en {output_file}")

if __name__ == "__main__":
    main()
