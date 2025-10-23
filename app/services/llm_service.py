import os
from zhipuai import ZhipuAI

# 从.env文件中加载并初始化智谱AI客户端
# (这部分代码保持不变)
client = ZhipuAI(api_key=os.getenv("ZHIPUAI_API_KEY"))

def generate_passphrase_from_llm(keywords):

    if not keywords:
        return "请输入至少一个关键词。"
        
    keyword_str = ", ".join(keywords)
    
    # --- 这是修改的核心 ---
    # 我们指示AI将中文关键词作为“灵感”或“主题”，
    # 但最终的产出必须是英文的、超现实的、高熵的。
    prompt = f"""
    你是一个精通密码学和计算语言学的安全专家。
    你的任务是创造“高熵可记忆英文口令”(High-Entropy Mnemonic English Passphrases)。

    【用户输入】
    用户将提供中文关键词作为“灵感主题”：【{keyword_str}】

    【你的任务流程】
    1.  **内部理解**：首先，理解用户提供的中文关键词【{keyword_str}】的核心含义。
    2.  **英文创作**：然后，围绕这些含义，创作一个【纯英文】的密码短语。

    【英文短语的安全生成规则】
    1.  **【拒绝陈词滥调】**：绝对禁止使用任何已知的、常见的英文短语、谚语、歌词、名言警句（例如："to be or not to be", "I love you"）。
    2.  **【强化结构熵】**：生成的英文短语必须在逻辑上是跳跃的、超现实的、非线性的（例如："Three dolphins repair clocks in the desert"），使其在统计上完全不可预测。
    3.  **【融合主题】**：必须将中文关键词的“含义”巧妙地融合到你创作的英文短语中。
    4.  **【保证可用性】**：整个英文短语必须在语法上是通顺的，可以被清晰地阅读和记忆。
    5.  **【长度要求】**：最终的英文短语长度应在 6 到 10 个单词之间。

    请现在开始你的创作。
    请不要重复我的指令或进行任何解释，不要包含任何中文，【直接输出你创作的那个唯一的英文密码短语】。
    """
    # --- 修改结束 ---
    
    try:
        response = client.chat.completions.create(
            model="glm-4",  # 强大的模型更适合这种复杂的、跨语言的创造性任务
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        # 清理AI可能返回的多余的引号或换行
        passphrase = response.choices[0].message.content.strip().strip('"')
        return passphrase
    except Exception as e:
        print(f"调用LLM API时出错: {e}")
        return "Sorry, an error occurred while generating the passphrase. Please try again."

def get_embedding_from_llm(text):
    """
    调用大模型获取文本的语义向量。
    (此函数功能明确，无需修改，是正确的。它可以很好地处理中文。)
    """
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

# --- 用于快速测试修改后效果的代码 ---
if __name__ == '__main__':
    print("--- 测试强化后的【英文】密码短语生成 ---")
    # 即使输入中文关键词
    test_keywords = ["月光", "代码", "海洋"]
    passphrase = generate_passphrase_from_llm(test_keywords)
    print(f"中文关键词: {test_keywords}")
    print(f"生成的英文短语: {passphrase}\n")
    
    test_keywords_2 = ["火焰", "猫", "图书馆"]
    passphrase_2 = generate_passphrase_from_llm(test_keywords_2)
    print(f"中文关键词: {test_keywords_2}")
    print(f"生成的英文短N语: {passphrase_2}\n")

    print("--- 测试语义向量获取 (中文) ---")
    test_text_chinese = "我大学毕业旅行去了青海湖，看到了美丽的日出。"
    vector = get_embedding_from_llm(test_text_chinese)
    if vector:
        print(f"获取中文向量成功，维度: {len(vector)}")
        print(f"向量前5维: {vector[:5]}")
    else:
        print("获取中文向量失败。")