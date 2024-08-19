import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
import speech_recognition as sr

def convertir_a_wav(archivo):
    formato = archivo.split('.')[-1]
    audio = AudioSegment.from_file(archivo, format=formato)
    wav_archivo = archivo.replace(f".{formato}", ".wav")
    audio.export(wav_archivo, format="wav")
    return wav_archivo

def transcribir_audio(archivo):
    try:
        wav_archivo = convertir_a_wav(archivo)
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_archivo) as source:
            audio = recognizer.record(source)
        texto = recognizer.recognize_google(audio, language="es-ES")
        print("Transcripción:", texto)
    except Exception as e:
        print("Error al procesar el archivo de audio:", e)

def seleccionar_archivo():
    archivo = filedialog.askopenfilename(
        filetypes=[("Archivos de audio", "*.mp3 *.wav *.ogg")]
    )
    if archivo:
        transcribir_audio(archivo)

root = tk.Tk()
root.title("Transcriptor de Audio")

boton_seleccionar = tk.Button(root, text="Seleccionar archivo", command=seleccionar_archivo)
boton_seleccionar.pack()

root.mainloop()
