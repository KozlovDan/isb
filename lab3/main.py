import argparse
from asymmetric_crypto import *
from symmetric_crypto import *
from file_utils import *


def generate_keys_mode(config: dict):
    """
    Режим генерации ключей.
    Генерирует пару RSA ключей, симметричный 3DES ключ,
    сохраняет их в файлы и шифрует симметричный ключ.
    """
    try:
        print("Генерация ключей...")
        private_key, public_key = generate_keys()
        save_keys(private_key, public_key, config['paths']['public_key'], config['paths']['private_key'])

        sym_key = generate_3des_key(config['algorithm']['key_length'])
        save_bytes_to_file(sym_key, config['paths']['symmetric_key'])

        encrypted_sym_key = encrypt_symmetric_key(sym_key, public_key)
        save_bytes_to_file(encrypted_sym_key, config['paths']['encrypted_symmetric_key'])
        print("Ключи успешно сгенерированы!")
    except RuntimeError as e:
        print(f"Ошибка генерации ключей: {str(e)}")
        exit(1)


def encrypt_mode(config: dict):
    """Режим шифрования данных.
        Читает исходные данные из файла, указанного в конфигурации,
        шифрует их с помощью симметричного ключа и сохраняет результат."""
    try:
        print("Шифрование данных...")
        private_key = load_private_key(config['paths']['private_key'])
        encrypted_sym_key = read_bytes_from_file(config['paths']['encrypted_symmetric_key'])

        sym_key = decrypt_symmetric_key(encrypted_sym_key, private_key)
        plaintext = read_text_from_file(config['paths']['initial_file'])

        encrypted_data = encrypt_data(plaintext.encode(), sym_key)
        save_bytes_to_file(encrypted_data, config['paths']['encrypted_file'])
        print("Данные успешно зашифрованы!")
    except RuntimeError as e:
        print(f"Ошибка шифрования: {str(e)}")
        exit(1)


def decrypt_mode(config: dict):
    """
        Режим дешифрования данных.
        Читает зашифрованные данные из файла, указанного в конфигурации,
        расшифровывает их с помощью симметричного ключа и сохраняет результат.
    """
    try:
        print("Дешифрование данных...")
        private_key = load_private_key(config['paths']['private_key'])
        encrypted_sym_key = read_bytes_from_file(config['paths']['encrypted_symmetric_key'])

        sym_key = decrypt_symmetric_key(encrypted_sym_key, private_key)
        encrypted_data = read_bytes_from_file(config['paths']['encrypted_file'])

        decrypted_data = decrypt_data(encrypted_data, sym_key)
        save_text_to_file(decrypted_data.decode(), config['paths']['decrypted_file'])
        print("Данные успешно расшифрованы!")
    except RuntimeError as e:
        print(f"Ошибка дешифрования: {str(e)}")
        exit(1)


if __name__ == "__main__":
    try:
        config = load_config()
        parser = argparse.ArgumentParser(description="Гибридная криптосистема (RSA + 3DES)")
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-gen', action='store_true', help='Генерация ключей')
        group.add_argument('-enc', action='store_true', help='Шифрование')
        group.add_argument('-dec', action='store_true', help='Дешифрование')

        args = parser.parse_args()
        match args:
            case argparse.Namespace(gen=True):
                generate_keys_mode(config)
            case argparse.Namespace(enc=True):
                encrypt_mode(config)
            case argparse.Namespace(dec=True):
                decrypt_mode(config)
    except argparse.ArgumentError:
        print("Ошибка: неверные аргументы командной строки")
        parser.print_help()
        exit(1)
    except RuntimeError as e:
        print(f"Ошибка при загрузке конфигурации: {str(e)}")
        exit(1)
