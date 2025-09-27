import os
from typing import Optional
from dotenv import load_dotenv
from resume_ai import llm_rewrite_prompt

load_dotenv()

def try_azure_rewrite(resume_text: str, jd_text: str) -> Optional[str]:
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    if not (endpoint and key and deployment):
        return None
    try:
        # Uses the official OpenAI SDK in Azure mode
        from openai import AzureOpenAI
        client = AzureOpenAI(
            api_key=key,
            api_version="2024-08-01-preview",
            azure_endpoint=endpoint
        )
        prompt = llm_rewrite_prompt(resume_text, jd_text)
        chat = client.chat.completions.create(
            model=deployment,
            messages=[{"role":"user","content":prompt}],
            temperature=0.2,
            max_tokens=600
        )
        return chat.choices[0].message.content.strip()
    except Exception as e:
        return f"Azure OpenAI call failed: {e}"
