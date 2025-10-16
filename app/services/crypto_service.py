import json
import numpy as np
from argon2 import PasswordHasher
from sklearn.metrics.pairwise import cosine_similarity

# 初始化Argon2密码哈希器
ph = PasswordHasher()

def hash_passphrase(passphrase):
    """使用Argon2对密码短语进行哈希"""
    return ph.hash(passphrase)

def verify_passphrase(hashed_passphrase, passphrase):
    """验证密码短语是否与哈希值匹配"""
    try:
        return ph.verify(hashed_passphrase, passphrase)
    except Exception:
        return False

def calculate_similarity(vec1, vec2):
    """计算两个向量的余弦相似度"""
    if vec1 is None or vec2 is None:
        return 0.0
    
    # 将向量列表转换为NumPy数组并重塑为2D
    vec1_reshaped = np.array(vec1).reshape(1, -1)
    vec2_reshaped = np.array(vec2).reshape(1, -1)
    
    # 计算相似度
    similarity_score = cosine_similarity(vec1_reshaped, vec2_reshaped)[0][0]
    return similarity_score

def serialize_vector(vector):
    """将向量列表序列化为JSON字符串以便存入数据库"""
    if vector is None:
        return None
    return json.dumps(vector)

def deserialize_vector(vector_json):
    """将JSON字符串反序列化为向量列表"""
    if vector_json is None:
        return None
    return json.loads(vector_json)