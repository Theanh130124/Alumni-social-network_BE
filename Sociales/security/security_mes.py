from cryptography.fernet import Fernet
# key = Fernet.generate_key()
# print(key)
MY_AES_KEY = b'vvK-iIKhYjaSPBUDiJmSFTUCN78wJWme-4Ot9TsDKWo='

# Mã hóa
def encode_aes(text):
    """
    Mã hóa chuỗi văn bản bằng Fernet.
    :param text: Chuỗi cần mã hóa
    :return: Chuỗi đã mã hóa (string)
    """
    fernet = Fernet(MY_AES_KEY)
    b_text = str(text).encode()  # Chuyển thành byte
    text_encrypt = fernet.encrypt(b_text).decode()  # Mã hóa -> về string
    return text_encrypt

# Giải mã
def decode_aes(text):
    fernet = Fernet(MY_AES_KEY)
    try:
        print(f"Decoding text: {text}")  # Debug
        b_text = text.encode() if isinstance(text, str) else text
        text_decrypt = fernet.decrypt(b_text).decode()
        return text_decrypt
    except Exception as e:
        print(f"Decode error: {e}")  # Debug lỗi giải mã
        return None
