# Use a imagem base do Ubuntu LTS
FROM ubuntu:22.04

# Atualizar o sistema e instalar ferramentas básicas
RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    curl \
    wget \
    libffi-dev \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    liblzma-dev \
    tk-dev \
    tcl-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar Python 3.11.3
RUN wget https://www.python.org/ftp/python/3.11.3/Python-3.11.3.tgz && \
    tar -xvf Python-3.11.3.tgz && \
    cd Python-3.11.3 && \
    ./configure --enable-optimizations && \
    make && \
    make install && \
    cd .. && \
    rm -rf Python-3.11.3 Python-3.11.3.tgz

# Atualizar pip para a última versão
RUN python3.11 -m ensurepip && python3.11 -m pip install --upgrade pip

# Instalar bibliotecas Qt e outras dependências gráficas
RUN apt-get update && apt-get install -y \
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
    libx11-xcb1 \
    libqt5widgets5 \
    x11-apps \
    x11-utils \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN pip install poetry

# Configurar o Poetry para não criar ambientes virtuais
ENV POETRY_VIRTUALENVS_CREATE=false

# Configurar variáveis de ambiente do Qt
ENV QT_DEBUG_PLUGINS=1
ENV QT_QPA_PLATFORM=xcb

# Definir o diretório de trabalho
WORKDIR /src

# Copiar o código-fonte para o container
COPY . .

# Instalar dependências com o Poetry
RUN poetry init --no-interaction --name tcc-daniel-app && \
    poetry add opencv-python PyQt5 numpy spidev RPi.GPIO

# Definir o comando padrão para executar o programa
ENTRYPOINT ["poetry", "run", "python3.11", "TCC_DANIEL/Prog/aplication.py"]
