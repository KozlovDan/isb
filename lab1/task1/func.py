import json


def open_file(filename: str) -> str:
    """Читает текстовый файл и возвращает его содержимое."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Файд {filename} не найден")
    except Exception as e:
        print(f"Файд {e} не может быть открыт")


def save_file(filename: str, content: str) -> None:
    """Записывает текст в файл."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Файд {e} не может быть создан")


def open_json(filename: str) -> dict:
    """Загружает JSON-файл. """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файд {filename} не найден")
    except Exception as e:
        print(f"Файд {e} не может быть открыт")


def save_json(filename: str, data: dict) -> None:
    """Сохраняет данные в JSON-файл."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Файд {e} не может быть создан")