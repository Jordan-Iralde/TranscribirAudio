import speech_recognition as sr
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def transcribir_audio(archivo):
    # Inicializa el reconocedor
    recognizer = sr.Recognizer()
    
    # Cargar el archivo de audio
    with sr.AudioFile(archivo) as source:
        audio = recognizer.record(source)  # Lee todo el archivo

    # Intenta reconocer el audio
    try:
        texto = recognizer.recognize_google(audio, language="es-ES")
        print("Transcripción:")
        print(texto)
    except sr.UnknownValueError:
        print("No se pudo entender el audio")
    except sr.RequestError as e:
        print(f"No se pudo conectar al servicio de reconocimiento; {e}")

def seleccionar_archivo():
    Tk().withdraw()  # Cierra la ventana de Tkinter
    archivo = askopenfilename(filetypes=[("Audio Files", "*.wav")])
    if archivo:
        transcribir_audio(archivo)
    else:
        print("No se seleccionó ningún archivo")

if __name__ == "__main__":
    seleccionar_archivo()
