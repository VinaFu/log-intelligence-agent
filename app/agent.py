from .tools import extract_keywords, generate_title, summarize_text, llm_summarize, analyze_errors_with_llm

class Agent:
    def __init__(self):
        self.tools = {
            "summarize": summarize_text,
            "llm_summarize": llm_summarize,
            "keywords": extract_keywords,
            "title": generate_title,
            "error_analysis": analyze_errors_with_llm 
        }

    def run_task(self, task: dict) -> dict:
        input_text = task.get("input", "")
        errors = task.get("errors", [])

        result = {}
        
        if input_text:
            result["summary"] = self.tools["summarize"](input_text)
            result["keywords"] = self.tools["keywords"](input_text)
            result["title"] = self.tools["title"](result["summary"])

        if errors:
            result["error_analysis"] = self.tools["error_analysis"](errors,top_n=3)
    
        if not result:
            return {"error": "Input text is required."}

        return result

