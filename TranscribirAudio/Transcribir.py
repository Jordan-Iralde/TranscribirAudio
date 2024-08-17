import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
from tkinter import Tk, filedialog
import os
from concurrent.futures import ThreadPoolExecutor
import tempfile

def transcribe_chunk(chunk, recognizer, index):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        chunk.export(temp_file.name, format="wav")
        temp_file_path = temp_file.name  # Guardar la ruta para eliminar después

    with sr.AudioFile(temp_file_path) as source:
        audio_listened = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio_listened, language='es-ES')
        print(f"Texto del segmento {index}: {text}")
    except sr.RequestError as e:
        text = f"Error en la solicitud al servicio de reconocimiento: {e}"
    except sr.UnknownValueError:
        text = f"No se pudo reconocer el audio del segmento {index}"
    finally:
        os.remove(temp_file_path)  # Eliminar el archivo temporal fuera del bloque "with"

    return text

def transcribe_audio(file_path, chunk_length_ms=60000, output_file="transcription.txt"):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(file_path)
    chunks = make_chunks(audio, chunk_length_ms)

    full_text = []

    with ThreadPoolExecutor() as executor:
        results = executor.map(lambda i: transcribe_chunk(chunks[i], recognizer, i), range(len(chunks)))

    full_text = " ".join(results)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_text.strip())

    print(f"Transcripción completa guardada en {output_file}")

def select_audio_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Selecciona un archivo de audio", filetypes=[("Audio Files", "*.wav *.flac *.mp3")])
    if file_path:
        output_file = filedialog.asksaveasfilename(title="Guardar transcripción como", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if output_file:
            transcribe_audio(file_path, output_file=output_file)
        else:
            print("No se seleccionó un archivo de salida para la transcripción.")
    else:
        print("No se seleccionó ningún archivo")

if __name__ == "__main__":
    select_audio_file()
