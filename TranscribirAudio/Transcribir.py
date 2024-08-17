import yt_dlp
import os
import speech_recognition as sr
from pydub import AudioSegment

def download_youtube_video(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': 'C:/ProgramData/chocolatey/bin',  # Asegúrate de usar la ruta correcta
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info_dict)
        return file_name

def extract_audio(video_path, audio_format='mp3'):
    if video_path is None:
        raise ValueError("El camino del video es None")
    audio_path = video_path.replace(".mp4", f".{audio_format}")
    if not os.path.isfile(audio_path):
        # Extrae el audio del video usando pydub
        video = AudioSegment.from_file(video_path)
        video.export(audio_path, format=audio_format)
    return audio_path

def transcribe_youtube_link(url):
    video_path = download_youtube_video(url)
    if video_path:
        audio_path = extract_audio(video_path, audio_format='mp3')
        return f"Audio extraído en: {audio_path}"
    else:
        return "No se pudo descargar el video."

def transcribe_audio_file(file_path):
    recognizer = sr.Recognizer()
    
    # Verificar la extensión del archivo
    if file_path.endswith('.mp3'):
        audio = AudioSegment.from_mp3(file_path)
        audio_path = file_path.replace('.mp3', '.wav')
        audio.export(audio_path, format='wav')
    else:
        audio_path = file_path

    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='es-ES')
            return text
    except sr.UnknownValueError:
        return "Google Speech Recognition no pudo entender el audio"
    except sr.RequestError as e:
        return f"No se pudo solicitar resultados a Google Speech Recognition; {e}"
    except Exception as e:
        return f"Ocurrió un error: {e}"

def main():
    url = input("Ingrese el enlace de YouTube o 'skip' para transcribir un archivo local: ")
    if url.lower() != 'skip':
        transcribed_text = transcribe_youtube_link(url)
        print(transcribed_text)
    else:
        file_path = input("Ingrese el camino del archivo de audio local (mp3 o wav): ")
        if os.path.isfile(file_path):
            transcribed_text = transcribe_audio_file(file_path)
            print("Texto transcrito:")
            print(transcribed_text)
        else:
            print("El archivo especificado no existe.")
while True:
    if __name__ == "__main__":
        main()
