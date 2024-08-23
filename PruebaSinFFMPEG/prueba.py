import speech_recognition as sr
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor

def convertir_a_wav(archivo):
    formato = archivo.split('.')[-1].lower()
    if formato in ["mp3", "ogg"]:
        audio = AudioSegment.from_file(archivo, format=formato)
        archivo_wav = archivo.replace(f".{formato}", ".wav")
        audio.export(archivo_wav, format="wav")
        return archivo_wav
    return archivo

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

def transcribir_audio_por_chunks(archivo, duracion_chunk=10, solapamiento=0.5):
    archivo = convertir_a_wav(archivo)
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(archivo) as source:
        total_duration = int(source.DURATION)
        chunks = []
        for i in range(0, total_duration, duracion_chunk - int(solapamiento)):
            audio_chunk = recognizer.record(source, duration=duracion_chunk)  # Lee el fragmento
            chunks.append((recognizer, audio_chunk, i//duracion_chunk + 1))

        with ThreadPoolExecutor() as executor:
            resultados = executor.map(lambda x: transcribir_chunk(*x), chunks)

        transcripcion_completa = " ".join(resultados)
        print("\nTranscripción completa:")
        print(transcripcion_completa)

def seleccionar_archivo():
    Tk().withdraw()  # Cierra la ventana de Tkinter
    archivo = askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3;*.ogg")])
    if archivo:
        transcribir_audio_por_chunks(archivo)
    else:
        print("No se seleccionó ningún archivo")

if __name__ == "__main__":
    seleccionar_archivo()
