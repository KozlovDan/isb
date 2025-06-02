import os
import json
from cryptography.hazmat.primitives.serialization import load_pem_private_key

def load_config(config_path: str = 'settings.json') -> dict:
    """
    Загрузка конфигурации из JSON файла.
    :param config_path: Путь к файлу конфигурации.
    :return: Загруженная конфигурация.
    """
    try:
        with open(config_path) as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл конфигурации {config_path} не найден")
    except json.JSONDecodeError:
        raise ValueError(f"Некорректный формат файла {config_path}")
    except Exception as e:
        raise RuntimeError(f"Ошибка загрузки конфигурации: {str(e)}")

def save_bytes_to_file(data: bytes, filename: str):
    """
    Сохранение бинарных данных в файл.
    :param data: Данные для сохранения.
    :param filename: Имя файла для сохранения.
    """
    try:
        with open(filename, 'wb') as f:
            f.write(data)
    except Exception as e:
        raise RuntimeError(f"Ошибка сохранения файла {filename}: {str(e)}")

def read_bytes_from_file(filename: str) -> bytes:
    """
    Чтение бинарных данных из файла.
    :param filename: Имя файла для чтения.
    :return: Прочитанные данные.
    """
    try:
        with open(filename, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {filename}")
    except Exception as e:
        raise RuntimeError(f"Ошибка чтения файла {filename}: {str(e)}")

def save_text_to_file(text: str, filename: str):
    """
    Сохранение текста в файл.
    :param text: Текст для сохранения.
    :param filename: Имя файла для сохранения.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        raise RuntimeError(f"Ошибка сохранения текста в {filename}: {str(e)}")

def read_text_from_file(filename: str) -> str:
    """
    Чтение текста из файла.
    :param filename: Имя файла для чтения.
    :return: Прочитанный текст.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        raise FileNotFoundError(f"Ошибка декодирования файла {filename}")
    except Exception as e:
        raise RuntimeError(f"Ошибка чтения текста из {filename}: {str(e)}")

def load_private_key(key_path: str, password: bytes = None):
    """
    Загрузка закрытого ключа из файла.
    :param key_path: Путь к файлу с ключом.
    :param password: Пароль для расшифровки ключа.
    :return: Загруженный приватный ключ.
    """
    try:
        key_data = read_bytes_from_file(key_path)
        return load_pem_private_key(key_data, password=password)
    except ValueError as e:
        raise ValueError(f"Неверный формат ключа: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Ошибка загрузки ключа: {str(e)}")