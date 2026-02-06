import os
from openai import OpenAI
import jieba
import re

# 实际功能实现的地方，比如：文本摘要、关键词提取、标题生成 → 主要业务逻辑写这里

#  client = OpenAI(api_key=os.getenv("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"))
#  export OPENAI_API_KEY="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"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(text: str) -> str:
    if len(text) <= 50:
        return text
    return text[:50] + "..." 


def llm_summarize(text:str) -> str:
    # GPT 摘要
    if not text.strip():
        return "No text provided!"

    try:
        response = client.chat.completions.create(model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
        ],
        max_tokens=150)
        summary = response.choices[0].message.content.strip()
        return summary

    except Exception as e:
        return f"An error occurred: {e}"

# 中文/英文 关键词抽取    
def extract_keywords(text: str) -> str:
    if not text.split():
        return "No text provided!"

    # 检查是否包含中文
    if re.search(r'[\u4e00-\u9fff]',text):
        words = jieba.lcut(text)
        keywords = [w for w in words if len(w)>1]
    else:
        words = text.split()
        keywords = [w for w in words if len(w)>4]

#     unique_words = set(words).  ??? + why 4?
#    keywords = [word for word in words if len(word) > 4]

    return " ".join(keywords) if keywords else "No keywords found."

# GPT 生成标题
def generate_title(text: str) -> str:
    if not text.strip():
        return "无标题" if re.search(r'[\u4e00-\u9fff]',text) else "No text provided!"

    # 检查是否包含中文
    if re.search(r'[\u4e00-\u9fff]',text):
        words = jieba.lcut(text)
        return "".join(words[:5]) + "..." if words else "无标题"
    else:
        words = text.split()
        return " ".join(words[:5]) + "..." if words else "No title"
  

    # try:
    #     response = client.chat.completions.create(model="gpt-4o-mini",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant that generates titles."},
    #         {"role": "user", "content": f"Generate a concise title for the following text:\n\n{text}"}
    #     ],
    #     max_tokens=20)
    #     title = response.choices[0].message.content.strip()
    #     return title

    # except Exception as e:
    #     return f"An error occurred: {e}"
