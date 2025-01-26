C:\Users\vinic\AppData\Local\Programs\Python\Python311\Scripts
C:\Users\vinic\AppData\Local\Programs\Python\Python311

Instalei o Python 3.11.3
Instalei o pip
Coloquei o Python no Path do Windows
Instalei a biblioteca de leitura do Python do QT Creator: PyQt5
Instalei a biblioteca do OpenCV para Python: cv2 (pip install opencv-python)
Instalei a biblioteca para comunicação SPI: spidev (pip install spidev)

run to create the virtual environment: uv venv --python 3.11.3
add opencv-python to this repository
uv pip install pyqt5 to install PyQt5, I wasn't able to add directly from UV
commented import spidev and import RPi.GPIO, because both are for linux and the code was designed to run in a Raspberry PI 3