import subprocess
import sys

FFMPEG_PATH = r'C:\ProgramData\chocolatey\bin\ffmpeg.exe'
FFPROBE_PATH = r'C:\ProgramData\chocolatey\bin\ffprobe.exe'

def check_ffmpeg_installed():
    try:
        subprocess.run([FFMPEG_PATH, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run([FFPROBE_PATH, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("ffmpeg y ffprobe están instalados y listos para usar.")
    except FileNotFoundError:
        print("ffmpeg o ffprobe no están instalados. Instalando...")
        install_ffmpeg()

def install_ffmpeg():
    try:
        subprocess.run(['choco', '--version'], check=True)
        print("Instalando ffmpeg...")
        subprocess.run(['choco', 'install', 'ffmpeg', '-y'], check=True)
    except FileNotFoundError:
        print("Chocolatey no está instalado. Instala Chocolatey primero.")
        sys.exit(1)

def main():
    check_ffmpeg_installed()
    print("ffmpeg está instalado y listo para usar.")

if __name__ == "__main__":
    main()
