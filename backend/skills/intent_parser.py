import json
from typing import Dict, Any, List

class IntentParsingSkill:
    """
    Skill for extracting tasks, locations, and time constraints from natural language.
    This will interact with the LLM (Qwen) to structure the user's messy prompt.
    """
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        
    def generate_parsing_prompt(self, user_input: str) -> str:
        return f"""
        You are an expert intent parser. The user wants to run a series of errands.
        Extract the following information from the user's input and output ONLY valid JSON.
        
        Required JSON Structure:
        {{
            "start_location": "Where the user is starting from (if unspecified, use 'current location')",
            "end_location": "Where the user wants to end up (if unspecified, use 'start_location')",
            "errands": [
                {{
                    "task": "Description of what they need to do (e.g., 'buy milk', 'dry cleaning')",
                    "category": "Broad category (e.g., 'grocery', 'laundry', 'bank')",
                    "preferred_time": "Any time constraints mentioned (e.g., 'before 5pm'). Null if none."
                }}
            ]
        }}
        
        User Input: "{user_input}"
        """
        
    def parse(self, user_input: str, qwen_api_key: str = None, gmi_cloud_api_key: str = None) -> Dict[str, Any]:
        """
        Execute the parsing skill using GMI Cloud API for testing.
        """
        prompt = self.generate_parsing_prompt(user_input)
        
        # --- Qwen Implementation (Commented out for now) ---
        # response = dashscope.Generation.call(
        #     model='qwen-turbo',
        #     prompt=prompt,
        #     api_key=qwen_api_key
        # )
        # return json.loads(response.output.text)
        
        # --- GMI Cloud API Implementation ---
        if gmi_cloud_api_key:
            import requests
            headers = {
                "Authorization": f"Bearer {gmi_cloud_api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "Qwen/Qwen3.7-Max",
                "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"}
            }
            # Note: Update URL if GMI Cloud provides a different base endpoint
            response = requests.post("https://api.gmi-serving.com/v1/chat/completions", headers=headers, json=data)
            
            if response.status_code == 200:
                content = response.json()["choices"][0]["message"]["content"]
                return json.loads(content)
            else:
                print(f"[IntentParser Error] {response.text}")
                return {"error": "GMI Cloud API Failed"}
        
        # Mock Response for structural completeness
        return {
            "start_location": "Home",
            "end_location": "Home",
            "errands": []
        }
