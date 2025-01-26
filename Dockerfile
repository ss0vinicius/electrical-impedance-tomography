# Base image
FROM python:3.11.3

# Update system and install necessary tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libgpiod-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
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

# Expose the application port (if required)
#EXPOSE 8501

# Default command to run the application
CMD ["python", "TCC_DANIEL/Prog/aplication.py"]
