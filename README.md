# Python 3.11.3 Setup and Dependencies

## Installations
- Installed **Python 3.11.3**
- Installed **pip**
- Added Python to **Windows PATH**
- Installed **PyQt5** (Python binding for Qt Creator)
- Installed **OpenCV** for Python: `pip install opencv-python`
- Installed **SPI communication library**: `pip install spidev`

## Running on Raspberry Pi 4 (Without Virtual Environment)
I was only able to run the project on **Raspberry Pi 4** without a virtual environment. I had to install dependencies directly using:
```sh
sudo apt install python3-numpy
sudo apt install python3-spidev
sudo apt install python3-opencv
sudo apt install python3-PyQt5
```

The **RPi.GPIO** library was installed using `poetry`, and it seems to be working fine.

---

## Learnings and Challenges
- **X11 Graphics Issues:**
  - I had many problems with the **X11 graphics library**.
  - **X11 is being deprecated** in favor of Wayland, but **Debian (and Raspberry Pi OS) still use X11**.
  - The code uses X11 for GUI rendering, so X11 must be properly enabled and functional.

- **PyQt5 Installation Issues:**
  - The only successful installation method was:
    ```sh
    sudo apt install python3-PyQt5
    ```
  - Other methods (Poetry, UV, Docker, Pip) **did not work** and caused issues.


## Virtual Environment Setup (I tried Docker, UV, Poetry, pyenv, but I had problems running GUI on it.)
Run the following command to create a virtual environment:
```sh
uv venv --python 3.11.3
```

### Additional Steps
- Added `opencv-python` to the repository.
- Installed PyQt5 manually:
  ```sh
  uv pip install pyqt5
  ```
  (Direct installation via UV was unsuccessful.)
- Commented out:
  ```python
  import spidev
  import RPi.GPIO
  ```
  (These libraries are for Linux and the code is designed to run on a Raspberry Pi 3, in Raspbian SO.)

---
