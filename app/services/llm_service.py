import os
from zhipuai import ZhipuAI

# 从.env文件中加载并初始化智谱AI客户端
client = ZhipuAI(api_key=os.getenv("ZHIPUAI_API_KEY"))

def generate_passphrase_from_llm(keywords):
    """根据关键词列表调用大模型生成密码短语"""
    if not keywords:
        return "请输入至少一个关键词。"
        
    keyword_str = ", ".join(keywords)
    prompt = f"请围绕关键词【{keyword_str}】，创作一个独特、富有想象力且易于记忆的中文密码短语。"
    
    try:
        response = client.chat.completions.create(
            model="glm-4",  # 你也可以使用 glm-3-turbo 获得更快的速度
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用LLM API时出错: {e}")
        return "抱歉，生成密码短语时出错，请稍后再试。"

def get_embedding_from_llm(text):
    """调用大模型获取文本的语义向量"""
    if not text:
        return None
        
    try:
        response = client.embeddings.create(
            model="embedding-2", # 智谱的向量模型
            input=text,
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"调用Embedding API时出错: {e}")
        return None