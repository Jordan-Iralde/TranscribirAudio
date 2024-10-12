import speech_recognition as sr
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor
import os

# Convierte el archivo de audio a formato WAV si es necesario
def convertir_a_wav(archivo):
    formato = archivo.split('.')[-1].lower()
    if formato in ["mp3", "ogg"]:
        audio = AudioSegment.from_file(archivo, format=formato)
        archivo_wav = archivo.replace(f".{formato}", ".wav")
        audio.export(archivo_wav, format="wav")
        return archivo_wav
    return archivo

# Función para transcribir un fragmento del audio
def transcribir_chunk(recognizer, audio_chunk, chunk_num):
    try:
        texto = recognizer.recognize_google(audio_chunk, language="es-ES")
        print(f"Transcripción del fragmento {chunk_num}: {texto}")
        return texto
    except sr.UnknownValueError:
        print(f"No se pudo entender el audio en el fragmento {chunk_num}")
        return ""
    except sr.RequestError as e:
        print(f"Error con el servicio de reconocimiento en el fragmento {chunk_num}; {e}")
        return ""

# Función para transcribir el archivo de audio por fragmentos (chunks)
def transcribir_audio_por_chunks(archivo, duracion_chunk=10, solapamiento=0.5):
    archivo = convertir_a_wav(archivo)  # Convierte el archivo si no es WAV
    recognizer = sr.Recognizer()

    # Nombre del archivo para la transcripción final
    nombre_txt = os.path.splitext(archivo)[0] + "_transcripcion.txt"
    
    with sr.AudioFile(archivo) as source:
        total_duration = int(source.DURATION)
        chunks = []
        
        # Recorre el archivo de audio y lo divide en fragmentos
        for i in range(0, total_duration, duracion_chunk - int(solapamiento)):
            audio_chunk = recognizer.record(source, duration=duracion_chunk)  # Lee el fragmento
            chunks.append((recognizer, audio_chunk, i // (duracion_chunk - int(solapamiento)) + 1))

        # Transcripción en paralelo usando múltiples hilos
        with ThreadPoolExecutor() as executor:
            resultados = executor.map(lambda x: transcribir_chunk(*x), chunks)

        # Une los resultados en una transcripción completa
        transcripcion_completa = " ".join(resultados)

        # Guarda la transcripción en un archivo de texto
        with open(nombre_txt, "w", encoding="utf-8") as f:
            f.write(transcripcion_completa)
        
        print(f"\nTranscripción completa guardada en: {nombre_txt}")

# Función para seleccionar el archivo de audio
def seleccionar_archivo():
    Tk().withdraw()  # Cierra la ventana de Tkinter
    archivo = askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3;*.ogg")])
    if archivo:
        transcribir_audio_por_chunks(archivo)
    else:
        print("No se seleccionó ningún archivo")

if __name__ == "__main__":
    seleccionar_archivo()
