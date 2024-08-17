import os
import subprocess
from pydub import AudioSegment
import speech_recognition as sr
import glob

def check_ffmpeg_installed():
    """Check if ffmpeg and ffprobe are available in the PATH."""
    try:
        # Check ffmpeg
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        # Check ffprobe
        subprocess.run(['ffprobe', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("ffmpeg and ffprobe are installed and accessible.")
    except FileNotFoundError as e:
        raise EnvironmentError("ffmpeg or ffprobe not found. Please ensure they are installed and added to the PATH.") from e
    except subprocess.CalledProcessError as e:
        raise EnvironmentError("ffmpeg or ffprobe returned an error. Please check the installation.") from e

def convert_to_wav(file_path):
    """
    Convert MP3 or other audio formats to WAV using pydub.
    """
    base, ext = os.path.splitext(file_path)
    wav_path = base + '.wav'
    
    if ext.lower() in ['.mp3', '.wav', '.ogg', '.flac']:
        try:
            audio = AudioSegment.from_file(file_path)
            audio.export(wav_path, format='wav')
            return wav_path
        except Exception as e:
            print(f"Error converting file {file_path}: {e}")
            return None
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

def transcribe_audio(file_path):
    """
    Transcribe audio file to text using Google Web Speech API.
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='es-ES')
            return text
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand the audio."
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition; {e}"

def process_file(file_path):
    """
    Process and transcribe a single audio file.
    """
    try:
        wav_path = convert_to_wav(file_path)
        if wav_path:
            print(f"Processing {wav_path}...")
            text = transcribe_audio(wav_path)
            os.remove(wav_path)  # Clean up temporary WAV file
            return file_path, text
        else:
            return file_path, "Error converting file."
    except Exception as e:
        return file_path, str(e)

def main():
  # Ensure ffmpeg and ffprobe are available
    
    # Define your audio files directory
    directory = 'downloads/*.mp3'  # Change this to your directory path
    files = glob.glob(directory)
    
    print(f"Found {len(files)} files.")
    
    results = []
    
    for file in files:
        file_path, text = process_file(file)
        results.append((file_path, text))
    
    # Print results
    for file, text in results:
        print(f"File: {file}")
        print(f"Transcription: {text}\n")

if __name__ == "__main__":
    main()
