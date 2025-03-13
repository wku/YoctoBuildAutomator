# Используем Ubuntu как базовый образ
FROM ubuntu:22.04

# Устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    git \
    bash \
    python3 \
    gawk \
    wget \
    diffstat \
    unzip \
    texinfo \
    gcc \
    build-essential \
    chrpath \
    socat \
    cpio \
    python3-pip \
    python3-pexpect \
    xz-utils \
    debianutils \
    iputils-ping \
    python3-git \
    python3-jinja2 \
    libegl1-mesa \
    libsdl1.2-dev \
    xterm \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем Python-скрипт в контейнер
COPY build_poky.py /app/

# Делаем скрипт исполняемым
RUN chmod +x /app/build_poky.py

# Устанавливаем точку входа
ENTRYPOINT ["python3", "/app/build_poky.py"]