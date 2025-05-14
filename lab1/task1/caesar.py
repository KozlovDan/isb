from func import *



def encrypt_caesar(text: str, shift: int, alphabet: str) -> str:
    """
    Шифрует текст алгоритмом Цезаря

    Args:
        text: Текст для шифрования
        shift: Величина сдвига (ключ)
        alphabet: Используемый алфавит

    Returns:
        Зашифрованный текст
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
    """Дешифрует текст алгоритмом Цезаря с заданным сдвигом"""
    decrypted = []
    for char in encrypted_text.upper():
        if char in alphabet:
            idx = (alphabet.index(char) - shift) % len(alphabet)
            decrypted.append(alphabet[idx])
        else:
            decrypted.append(char)
    return ''.join(decrypted)



def main():
    try:
        config = open_json("task1/config.json")
        text = open_file(config["original_text"])
        key = open_json(config["key"])

        encrypted_text = encrypt_caesar(text, key["shift"], config["alphabet"])
        save_file(config["encrypted_text"], encrypted_text)
    except Exception as e:
        print(f"Ошибка : {e} ")
    try:
        config = open_json("task1/config.json")
        text = open_file(config["encrypted_text"])
        key = open_json(config["key"])

        decrypted_text = decrypt_caesar(encrypted_text, key["shift"], config["alphabet"])
        save_file(config["decrypted_text"], decrypted_text)
    except Exception as e:
        print(f"Ошибка : {e} ")
    return 0


if __name__ == "__main__":
    main()
