# Base image
FROM RaspberryPiOS:latest
FROM python:3.11.3

# Update system and install necessary tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libgpiod-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    libxkbcommon-x11-0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-render-util0 \
    libxcb-render0 \
    libxcb-shape0 \
    libxcb-shm0 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxcb-randr0 \
    libxcb-util1 \
    libxcb-xkb1 \
    libqt5widgets5 \
    libx11-xcb1 \
    mesa-utils \
    x11-utils \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Set Poetry to not create a virtual environment
ENV POETRY_VIRTUALENVS_CREATE=false

# Copy the application code to the container
COPY . /src

# Set the working directory in the container
WORKDIR /src

# Initialize Poetry and add dependencies
RUN poetry init --no-interaction --name tcc-daniel-app && \
    poetry add opencv-python PyQt5 numpy spidev RPi.GPIO

# Configure Qt environment
ENV QT_DEBUG_PLUGINS=1
ENV QT_QPA_PLATFORM=xcb

# Correct ENTRYPOINT to run Python script
ENTRYPOINT ["poetry", "run", "python", "TCC_DANIEL/Prog/aplication.py"]
