# prompt_techniques.py

from typing import List, Dict
from app.services.post-service.openai-service import send_prompt_to_model


class PromptTechniqueProcessor:
    def __init__(self, model="gpt-4"):
        self.model = model

    def apply_techniques(self, base_prompt: str, techniques: List[str]) -> Dict[str, str]:
        responses = {}
        for technique in techniques:
            if hasattr(self, technique):
                prompt_variant = getattr(self, technique)(base_prompt)
                response = send_prompt_to_model(prompt_variant, model=self.model)
                responses[technique] = response
            else:
                responses[technique] = f"Technique '{technique}' not implemented."
        return responses

    # ---------------------------
    # FEW-SHOT TECHNIQUES
    # ---------------------------

    def few_shot_transform_to_question(self, prompt: str) -> str:
        return (
            "I want you to transform statements into questions. Here are some examples:\n"
            "Statement: 'I love pizza.' -> Question: 'Do I love pizza?'\n"
            "Statement: 'She went to the store.' -> Question: 'Did she go to the store?'\n"
            "Now, transform the following statement into a question:\n"
            f"Statement: '{prompt}'"
        )

    def few_shot_ask_intro_context_followup(self, prompt: str) -> str:
        return (
            "You are an assistant having a meaningful conversation.\n"
            "Start with a question to engage the user,\n"
            "provide some helpful context,\n"
            "then finish with a follow-up question.\n"
            f"Main topic: {prompt}"
        )

    def few_shot_compare_opinions(self, prompt: str) -> str:
        return (
            "Given the topic below, give two opposing opinions, and then a neutral summary.\n"
            f"Topic: {prompt}"
        )

    def few_shot_elaborate_then_simplify(self, prompt: str) -> str:
        return (
            "Take the following topic and first explain it in technical detail,\n"
            "then simplify it for a beginner.\n"
            f"Topic: {prompt}"
        )


# Optional: helper to list available techniques
    def list_available_techniques(self) -> List[str]:
        return [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("__") and not func.startswith("list_") and func != "apply_techniques"]
