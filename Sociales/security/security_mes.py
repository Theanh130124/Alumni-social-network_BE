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
    """
    Giải mã chuỗi đã mã hóa bằng Fernet.
    :param text: Chuỗi đã mã hóa (string)
    :return: Chuỗi sau khi giải mã (string)
    """
    fernet = Fernet(MY_AES_KEY)
    try:
        # Đảm bảo dữ liệu đầu vào là bytes trước khi giải mã
        b_text = text.encode() if isinstance(text, str) else text
        text_decrypt = fernet.decrypt(b_text).decode()  # Giải mã -> về string
        return text_decrypt
    except Exception as e:
        print(f"Decode error: {e}")
        return None
