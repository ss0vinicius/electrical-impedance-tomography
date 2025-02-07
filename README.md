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

Atualização:
só consegui rodar na Raspberry Pi 4 sem ambiente virtual, precisei instalar as dependências diretamente com sudo apt install python3-depencia:
sudo apt install python3-numpy
sudo apt install python3-spidev
sudo apt install python3-opencv
sudo apt install python3-PyQt5

a biblioteca RPi.GPIO eu instalei com o poetry e parece ter funcionado
Aprendizado: tive muitos problemas com a biblioteca gráfica X11 que tem sido despriorizada em relação a Wayland, mas o Debian ainda usa X11 e a Raspberry PI OS é baseada nele, então o código do Daniel utiliza o X11 para gerar a GUI e precisa estar com esta biblioteca habilitada e funcionando para que a GUI funcione corretamente.
Também tive muito problema com o PyQt5, só consegui instalar ele com o sudo apt install python3-PyQt5. De todos os outros jeitos (poetry, UV, Docker, pip) eu tive problemas e não funcionou.
