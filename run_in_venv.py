import os
import sys
import subprocess

# Определяем пути
venv_path = os.path.join(os.path.dirname(__file__), '.venv')
script_path = os.path.join(os.path.dirname(__file__), 'main.py')

# Проверяем ОС для определения правильного пути к Python в виртуальном окружении
if sys.platform == 'win32':
    python_executable = os.path.join(venv_path, 'Scripts', 'python.exe')
else:
    python_executable = os.path.join(venv_path, 'bin', 'python')

# Проверяем существование файлов
if not os.path.exists(python_executable):
    print(f"Ошибка: Не найден Python в виртуальном окружении по пути {python_executable}")
    sys.exit(1)

if not os.path.exists(script_path):
    print(f"Ошибка: Не найден файл main.py по пути {script_path}")
    sys.exit(1)

# Запускаем скрипт с помощью Python из виртуального окружения
try:
    subprocess.run([python_executable, script_path], check=True)
except subprocess.CalledProcessError as e:
    print(f"Ошибка при выполнении скрипта: {e}")
    sys.exit(1)
