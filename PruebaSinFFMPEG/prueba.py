import speech_recognition as sr
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def transcribir_audio_por_chunks(archivo, duracion_chunk=10):
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(archivo) as source:
        # Calcular el número de fragmentos que se necesitan
        total_duration = int(source.DURATION)
        for i in range(0, total_duration, duracion_chunk):
            source_audio = recognizer.record(source, duration=duracion_chunk)  # Lee el fragmento
            
            try:
                # Transcribe el fragmento de audio
                texto = recognizer.recognize_google(source_audio, language="es-ES")
                print(f"Transcripción del fragmento {i//duracion_chunk + 1}:")
                print(texto)
            except sr.UnknownValueError:
                print(f"No se pudo entender el audio en el fragmento {i//duracion_chunk + 1}")
            except sr.RequestError as e:
                print(f"Error con el servicio de reconocimiento en el fragmento {i//duracion_chunk + 1}; {e}")

def seleccionar_archivo():
    Tk().withdraw()  # Cierra la ventana de Tkinter
    archivo = askopenfilename(filetypes=[("Audio Files", "*.wav")])
    if archivo:
        transcribir_audio_por_chunks(archivo)
    else:
        print("No se seleccionó ningún archivo")

if __name__ == "__main__":
    seleccionar_archivo()
