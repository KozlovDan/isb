import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


def generate_3des_key(key_length: int = 192) -> bytes:
    """
    Генерация ключа для алгоритма 3DES.
    :param key_length: Длина ключа в битах.
    :return: Сгенерированный ключ.
    """
    match key_length:
        case 192:
            return os.urandom(24)
        case 128:
            return os.urandom(16)
        case 64:
            return os.urandom(8)
        case _:
            raise ValueError("Недопустимая длина ключа")


def encrypt_data(data: bytes, key: bytes) -> bytes:
    """
    Шифрование данных с использованием 3DES в режиме CBC.
    :param data: Данные для шифрования.
    :param key: Ключ шифрования.
    :return: Зашифрованные данные с добавленным вектором инициализации (IV).
    """
    iv = os.urandom(8)
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(64).padder()
    padded_data = padder.update(data) + padder.finalize()

    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext


def decrypt_data(encrypted_data: bytes, key: bytes) -> bytes:
    """
    Дешифрование данных, зашифрованных с использованием 3DES в режиме CBC.
    :param encrypted_data: Зашифрованные данные (IV + ciphertext).
    :param key: Ключ шифрования.
    :return: Расшифрованные данные.
    """
    iv, ciphertext = encrypted_data[:8], encrypted_data[8:]
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(64).unpadder()
    return unpadder.update(padded_data) + unpadder.finalize()