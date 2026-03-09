"""
BlackRoad GPT-4 API Wrapper
High-performance wrapper for OpenAI GPT-4 API
"""

import os
from typing import Optional, List, Dict, Any
from openai import OpenAI

class GPT4Wrapper:
    """Production-ready GPT-4 API wrapper for BlackRoad OS"""
    
    def __init__(self, api_key: Optional[str] = None, org_id: Optional[str] = None):
        self.client = OpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            organization=org_id or os.getenv("OPENAI_ORG_ID")
        )
        self.default_model = "gpt-4-turbo-preview"
        
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False
    ) -> str:
        """Send chat completion request"""
        response = self.client.chat.completions.create(
            model=model or self.default_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream
        )
        
        if stream:
            return response  # Return generator for streaming
        return response.choices[0].message.content
    
    def complete(self, prompt: str, **kwargs) -> str:
        """Simple completion interface"""
        messages = [{"role": "user", "content": prompt}]
        return self.chat(messages, **kwargs)
    
    def with_system(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Completion with system prompt"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        return self.chat(messages, **kwargs)
    
    def function_call(
        self,
        messages: List[Dict],
        functions: List[Dict],
        function_call: str = "auto"
    ) -> Dict[str, Any]:
        """Execute function calling"""
        response = self.client.chat.completions.create(
            model=self.default_model,
            messages=messages,
            tools=[{"type": "function", "function": f} for f in functions],
            tool_choice=function_call
        )
        return {
            "content": response.choices[0].message.content,
            "tool_calls": response.choices[0].message.tool_calls
        }


# Singleton instance for BlackRoad integration
_instance: Optional[GPT4Wrapper] = None

def get_gpt4() -> GPT4Wrapper:
    """Get or create GPT-4 wrapper instance"""
    global _instance
    if _instance is None:
        _instance = GPT4Wrapper()
    return _instance


if __name__ == "__main__":
    # Quick test
    gpt = GPT4Wrapper()
    response = gpt.complete("Say hello in one word")
    print(f"Response: {response}")
