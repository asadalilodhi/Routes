import os
# pyrefly: ignore [missing-import]
import dashscope
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()
qwen_api_key = os.getenv("QWEN_API_KEY")
gmi_cloud_api_key = os.getenv("GMI_CLOUD_API_KEY")

class ParserAgent:
    def __init__(self, parser_skill):
        self.parser_skill = parser_skill
        
    def execute(self, user_prompt: str) -> dict:
        print(f"[ParserAgent] Parsing user input: {user_prompt}")
        parsed = self.parser_skill.parse(user_input=user_prompt, qwen_api_key=qwen_api_key, gmi_cloud_api_key=gmi_cloud_api_key)
        print(f"[ParserAgent] Result: {parsed}")
        return parsed
