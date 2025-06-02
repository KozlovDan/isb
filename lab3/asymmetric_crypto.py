from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidKey
from file_utils import save_bytes_to_file


def generate_keys():
    """
    Генерация пары RSA ключей.
    :return: Кортеж (private_key, public_key).
    """
    try:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        return private_key, public_key
    except Exception as e:
        raise RuntimeError(f"Ошибка генерации ключей: {str(e)}")


def save_keys(private_key, public_key):
    """
    Сохранение RSA ключей в файлы.
    :param private_key: Приватный ключ для сохранения.
    :param public_key: Публичный ключ для сохранения.
    """
    try:
        # Закрытый ключ
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        save_bytes_to_file(private_pem, 'private.pem')

        # Открытый ключ
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        save_bytes_to_file(public_pem, 'public.pem')
    except Exception as e:
        raise RuntimeError(f"Ошибка сохранения ключей: {str(e)}")


def encrypt_symmetric_key(symmetric_key: bytes, public_key) -> bytes:
    """
    Шифрование симметричного ключа с использованием RSA.
    :param symmetric_key: Симметричный ключ для шифрования.
    :param public_key: Публичный RSA ключ.
    :return: Зашифрованный симметричный ключ.
    """
    try:
        return public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except (ValueError, InvalidKey) as e:
        raise ValueError(f"Ошибка шифрования ключа: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Неожиданная ошибка: {str(e)}")


def decrypt_symmetric_key(encrypted_key: bytes, private_key) -> bytes:
    """
    Дешифрование симметричного ключа с использованием RSA.
    :param encrypted_key: Зашифрованный симметричный ключ.
    :param private_key: Приватный RSA ключ.
    :return: Расшифрованный симметричный ключ.
    """
    try:
        return private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except (ValueError, InvalidKey) as e:
        raise ValueError(f"Ошибка дешифрования ключа: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Неожиданная ошибка: {str(e)}")