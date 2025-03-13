#!/usr/bin/env python3
import os
import subprocess
import shutil
import sys

# Параметры
WORK_DIR = "poky-build"
POKY_VERSION = "kirkstone"  # Укажите нужную ветку, например, "kirkstone" или "master"
MACHINE = "qemux86-64"      # Целевая машина
IMAGE = "core-image-minimal"  # Целевой образ

def run_command(command, cwd=None, use_bash=False):
    """Выполнение команды в shell с выводом результата"""
    shell = "/bin/bash" if use_bash else "/bin/sh"
    print(f"Выполняем команду: '{command}' в директории: {cwd or os.getcwd()}")
    result = subprocess.run(command, shell=True, executable=shell, cwd=cwd, text=True, capture_output=True)
    print(f"Код возврата: {result.returncode}")
    print(f"Вывод (stdout): {result.stdout}")
    if result.returncode != 0:
        print(f"Ошибка выполнения команды '{command}' (stderr): {result.stderr}")
        sys.exit(1)
    return result.stdout

def check_dependencies():
    """Проверка наличия необходимых зависимостей"""
    required_tools = ["git", "bash", "python3"]
    missing = []
    for tool in required_tools:
        if shutil.which(tool) is None:
            missing.append(tool)
    if missing:
        print(f"Ошибка: отсутствуют необходимые утилиты: {', '.join(missing)}")
        print("Установите их, например, на Ubuntu: sudo apt-get install git bash python3")
        sys.exit(1)
    print("Все зависимости найдены.")

def check_file_exists(file_path, description):
    """Проверка существования файла"""
    if not os.path.exists(file_path):
        print(f"Ошибка: {description} не найден по пути: {file_path}")
        sys.exit(1)
    print(f"{description} найден: {file_path}")

def check_dir_exists(dir_path, create_if_missing=False):
    """Проверка существования директории с опцией создания"""
    if not os.path.exists(dir_path):
        if create_if_missing:
            os.makedirs(dir_path)
            print(f"Создана директория: {dir_path}")
        else:
            print(f"Ошибка: директория не найдена: {dir_path}")
            sys.exit(1)
    else:
        print(f"Директория найдена: {dir_path}")


def setup_poky():
    """Настройка Poky"""
    check_dependencies()

    if not os.path.exists(WORK_DIR):
        print(f"Клонируем Poky ветку {POKY_VERSION}...")
        run_command(f"git clone -b {POKY_VERSION} git://git.yoctoproject.org/poky {WORK_DIR}")
    else:
        print(f"Директория {WORK_DIR} уже существует, пропускаем клонирование.")

    oe_init_path = os.path.abspath(os.path.join(WORK_DIR, "oe-init-build-env"))
    check_file_exists(oe_init_path, "Файл oe-init-build-env")

    build_dir = os.path.join(WORK_DIR, "build")
    conf_dir = os.path.join(build_dir, "conf")
    check_dir_exists(conf_dir, create_if_missing=True)

    local_conf_path = os.path.join(conf_dir, "local.conf")
    with open(local_conf_path, "a") as f:
        f.write(f'MACHINE = "{MACHINE}"\n')
        f.write('DISTRO = "poky"\n')
        f.write('BB_NUMBER_THREADS = "2"\n')  # Ограничение BitBake до 2 потоков
        f.write('PARALLEL_MAKE = "-j2"\n')    # Ограничение make до 2 ядер
        f.write('# Автоматически добавлено скриптом\n')
    check_file_exists(local_conf_path, "Файл local.conf")


def build_image():
    """Сборка образа с использованием временного скрипта в WORK_DIR"""
    oe_init_path = os.path.abspath(os.path.join(WORK_DIR, "oe-init-build-env"))
    temp_script = os.path.join(WORK_DIR, "build.sh")
    script_content = f"""#!/bin/bash
set -x  # Включаем отладку: показываем все команды
. {oe_init_path} build
bitbake {IMAGE}
"""
    print(f"Создаём временный скрипт: {temp_script}")
    with open(temp_script, "w") as f:
        f.write(script_content)
    os.chmod(temp_script, 0o755)
    try:
        run_command("./build.sh", cwd=WORK_DIR, use_bash=True)
    finally:
        os.remove(temp_script)
        print(f"Временный скрипт {temp_script} удалён.")

def clean_up():
    """Дополнительная функция для очистки"""
    if os.path.exists(WORK_DIR):
        shutil.rmtree(WORK_DIR)
        print(f"Директория {WORK_DIR} удалена.")
    else:
        print(f"Директория {WORK_DIR} не существует, ничего удалять не нужно.")

if __name__ == "__main__":
    print("Настройка Poky...")
    setup_poky()
    print("Запуск сборки...")
    build_image()
    print(f"Сборка {IMAGE} для {MACHINE} завершена!")
