import argparse
from utils.func import *



def encrypt_caesar(text: str, shift: int, alphabet: str) -> str:
    """
    Шифрует текст алгоритмом Цезаря с заданным сдвигом.

    :param encrypted_text: Текст для дешифрования
    :param shift: Величина сдвига
    :param alphabet: Используемый алфавит
    :return: Зашифрованная строка
    """
    encrypted = []
    for char in text.upper():
        if char in alphabet:
            idx = (alphabet.index(char) + shift) % len(alphabet)
            encrypted.append(alphabet[idx])
        else:
            encrypted.append(char)
    return ''.join(encrypted)

def decrypt_caesar(encrypted_text: str, shift: int, alphabet: str) -> str:
    """
    Дешифрует текст алгоритмом Цезаря с заданным сдвигом
    :param encrypted_text: Текст для дешифрования
    :param shift: Величина сдвига
    :param alphabet: Используемый алфавит
    :return: Зашифрованная строка
    """
    decrypted = []
    for char in encrypted_text.upper():
        if char in alphabet:
            idx = (alphabet.index(char) - shift) % len(alphabet)
            decrypted.append(alphabet[idx])
        else:
            decrypted.append(char)
    return ''.join(decrypted)

def parse_args():
    """
    Парсинг аргументов командной строки.
    :return:
    """
    parser = argparse.ArgumentParser(
        description="Программа для шифрования/дешифрования методом Цезаря"
    )
    parser.add_argument(
        'mode',
        choices=['encrypt', 'decrypt'],
        help='Режим работы: encrypt - шифрование, decrypt - дешифрование'
    )
    parser.add_argument(
        '-c', '--config',
        default='task1/config.json',
        help='Путь к файлу конфигурации (по умолчанию: task1/config.json)'
    )
    return parser.parse_args()



def main():
    args = parse_args()
    try:
        config = open_json(args.config)
        if args.mode == 'encrypt':
            text = open_file(config["original_text"])
            key = open_json(config["key"])
            result = encrypt_caesar(text, key["shift"], config["alphabet"])
            save_file(config["encrypted_text"], result)
            print("Текст успешно зашифрован")
        elif args.mode == 'decrypt':
            text = open_file(config["encrypted_text"])
            key = open_json(config["key"])
            result = decrypt_caesar(text, key["shift"], config["alphabet"])
            save_file(config["decrypted_text"], result)
            print("Текст успешно расшифрован")
        return 0
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
