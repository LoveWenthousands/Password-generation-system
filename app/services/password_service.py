import secrets
import string
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

def generate_random_password(length=16):
    """生成一个高强度的随机密码"""
    # 确保包含所有类型的字符
    chars = string.ascii_letters + string.digits + string.punctuation
    # 生成随机密码
    password = ''.join(secrets.choice(chars) for _ in range(length))
    return password

def get_encryption_key(master_password: str, salt: bytes = None) -> tuple[bytes, bytes]:
    """从主密码派生加密密钥"""
    if salt is None:
        salt = secrets.token_bytes(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key, salt

def encrypt_password(password: str, master_password: str, salt: bytes = None) -> tuple[bytes, bytes]:
    """使用主密码加密服务密码"""
    key, salt = get_encryption_key(master_password, salt)
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password, salt

def decrypt_password(encrypted_password: bytes, master_password: str, salt: bytes) -> str:
    """使用主密码解密服务密码"""
    key, _ = get_encryption_key(master_password, salt)
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password)
    return decrypted_password.decode()