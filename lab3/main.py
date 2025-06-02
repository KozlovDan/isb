import argparse
from asymmetric_crypto import *
from symmetric_crypto import *
from file_utils import *


def generate_keys_mode(config: dict):
    """Режим генерации ключей.

    Генерирует пару RSA ключей, симметричный 3DES ключ,
    сохраняет их в файлы и шифрует симметричный ключ."""
    try:
        print("Генерация ключей...")

        private_key, public_key = generate_keys()

        save_bytes_to_file(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ),
            config['secret_key']
        )

        save_bytes_to_file(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ),
            config['public_key']
        )

        sym_key = generate_3des_key(192)
        save_bytes_to_file(sym_key, config['symmetric_key'])

        print("Ключи успешно сгенерированы и сохранены!")
    except Exception as e:
        print(f"Ошибка генерации ключей: {str(e)}")
        exit(1)


def encrypt_mode(config: dict):
    """Режим шифрования данных.

    Читает исходные данные из файла, указанного в конфигурации,
    шифрует их с помощью симметричного ключа и сохраняет результат."""
    try:
        print("Шифрование данных...")

        private_key = load_private_key(config['secret_key'])
        sym_key = read_bytes_from_file(config['symmetric_key'])

        plaintext = read_text_from_file(config['initial_file'])
        encrypted_data = encrypt_data(plaintext.encode(), sym_key)

        save_bytes_to_file(encrypted_data, config['encrypted_file'])
        print("Данные успешно зашифрованы!")
    except Exception as e:
        print(f"Ошибка шифрования: {str(e)}")
        exit(1)


def decrypt_mode():
    """
    Режим дешифрования данных.

    Читает зашифрованные данные из файла, указанного в конфигурации,
    расшифровывает их с помощью симметричного ключа и сохраняет результат.
    """
    try:
        print("Дешифрование данных...")
        config = load_config()
        private_key = load_private_key('private.pem')
        encrypted_sym_key = read_bytes_from_file('symmetric.key.enc')

        sym_key = decrypt_symmetric_key(encrypted_sym_key, private_key)
        encrypted_data = read_bytes_from_file(config['encrypted_file'])

        decrypted_data = decrypt_data(encrypted_data, sym_key)
        save_text_to_file(decrypted_data.decode(), config['decrypted_file'])
        print("Данные успешно расшифрованы!")
    except Exception as e:
        print(f"Ошибка дешифрования: {str(e)}")
        exit(1)


if __name__ == "__main__":
    try:
        config = load_config()
    except Exception as e:
        print(f"Ошибка загрузки конфигурации: {str(e)}")
        exit(1)

    parser = argparse.ArgumentParser(description="Гибридная криптосистема (RSA + 3DES)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--gen', action='store_true', help='Генерация ключей')
    group.add_argument('--enc', action='store_true', help='Шифрование')
    group.add_argument('--dec', action='store_true', help='Дешифрование')

    args = parser.parse_args()

    # Выбор режима работы
    if args.gen:
        generate_keys_mode(config)
    elif args.enc:
        encrypt_mode(config)
    elif args.dec:
        decrypt_mode(config)
    else:
        parser.print_help()
        exit(1)