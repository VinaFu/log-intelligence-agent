from .tools import extract_keywords, generate_title, summarize_text, llm_summarize

# “调度中心”，管理和调用不同工具（tools） → 负责执行流程（Plan → Act → Observe）
class Agent:
    def __init__(self):
        self.tools = {
            "summarize": summarize_text,
            "llm_summarize": llm_summarize,
            "keywords": extract_keywords,
            "title": generate_title,
        }

        # 所以summarize和keywords分别是做什么的？是内置的吗？
        # 每post 一次，agent 会自动调用两个工具，返回json， 包括summary和keywords

    def run_task(self, task: dict) -> dict:
        input_text = task.get("input", "")
        
        if not input_text:
            return {"error": "Input text is required."}
        
        summary = self.tools["summarize"](input_text)
        keywords = self.tools["keywords"](input_text)
        title = self.tools["title"](summary)

        return {
            "summary": summary,
            "keywords": keywords,
            "title": title
        }
    

#     {"input": "这是一个需要总结的很长文本，其中包含一些重要关键词"}
#     {  "input": "This is a long text that needs to be summarized and from which we want to extract keywords."}
# {
#   "input": "This is a long text that needs to be summarized, keywords extracted, and a concise title generated."
# }

# {
#   "input": "这是一个需要总结的长文本，其中包含一些重要关键词，并希望生成一个简短标题。"
# }

