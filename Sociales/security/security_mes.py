from cryptography.fernet import Fernet
# key = Fernet.generate_key()
# print(key)
MY_AES_KEY = b'vvK-iIKhYjaSPBUDiJmSFTUCN78wJWme-4Ot9TsDKWo='

#Mã hóa
def encode_aes(text):
    fernet = Fernet(MY_AES_KEY)
    b_text = str(text).encode() #Chuyển thành byte
    text_encrypt = fernet.encrypt(b_text).decode() # mã hóa -> nhưng mã về string
    return text_encrypt

#Giai ma
def decode_aes(text):
    fernet = Fernet(MY_AES_KEY)
    text_decrypt = fernet.decrypt(text).decode() #giải mã -> giải về string
    return text_decrypt