import os
from openai import OpenAI
import jieba
import re

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(text: str) -> str:
    if len(text) <= 50:
        return text
    return text[:50] + "..." 


def llm_summarize(text:str) -> str:
    # GPT summary
    if not text.strip():
        return "No text provided!"

    try:
        response = client.chat.completions.create(model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
        ],
        max_tokens=150)
        summary = response.choices[0].message.content.strip()
        return summary

    except Exception as e:
        return f"An error occurred: {e}"

# Chinese/English keyword extraction   
def extract_keywords(text: str) -> str:
    if not text.split():
        return "No text provided!"

    # Check if the text contains Chinese characters
    if re.search(r'[\u4e00-\u9fff]',text):
        words = jieba.lcut(text)
        keywords = [w for w in words if len(w)>1]
    else:
        words = text.split()
        keywords = [w for w in words if len(w)>4]

    return " ".join(keywords) if keywords else "No keywords found."

# GPT Title generation (Chinese/English)
def generate_title(text: str) -> str:
    if not text.strip():
        return "无标题" if re.search(r'[\u4e00-\u9fff]',text) else "No text provided!"

    if re.search(r'[\u4e00-\u9fff]',text):
        words = jieba.lcut(text)
        return "".join(words[:5]) + "..." if words else "无标题"
    else:
        words = text.split()
        return " ".join(words[:5]) + "..." if words else "No title"

# ---------- Handle Error——JSON ----------
MAX_MSG_LEN = 200
MAX_TOKENS = 200 

def analyze_errors_with_llm(errors_json: dict, top_n: int = 3) -> dict:
    sorted_errors = sorted(errors_json.get("unique_errors", []),
                           key=lambda x: x["count"], reverse=True)
    top_errors = sorted_errors[:top_n]

    if not top_errors:
        return {"top_errors_with_solution": [], "all_errors_counts_sorted": {}}

    analyzed_top_errors = []

    for idx, e in enumerate(top_errors, start=1):
        msg_preview = e["message"][:MAX_MSG_LEN]
        batch_text = f"[{e['timestamp']}] [{e['module']}] [{e['thread']}] (occurred {e['count']} times) {msg_preview}"

        try:
            # call LLM to analyze this error and provide solution
            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Senior Java engineer. Analyze WildFly/JBoss errors. "
                            "Provide concise and exact solution based on message content."
                        )
                    },
                    {"role": "user", "content": f"Analyze this error:\n{batch_text}"}
                ],
                max_tokens=MAX_TOKENS,
            )
            solution = response.choices[0].message.content.strip()
        except Exception as ex:
            solution = f"LLM call failed: {ex}"

        analyzed_top_errors.append({
            "rank": idx,
            "count": e["count"],
            "timestamp": e["timestamp"],
            "module": e["module"],
            "thread": e["thread"],
            "message": e["message"],
            "solution": solution
        })

    counts_sorted = dict(sorted(errors_json.get("counts", {}).items(),
                                key=lambda item: item[1], reverse=True))

    return {
        "top_errors_with_solution": analyzed_top_errors,
        "all_errors_counts_sorted": counts_sorted
    }

