import os
from langchain_openai import ChatOpenAI
import httpx


class LLMService:
    def __init__(self, model=None):
        self.gateway_url = os.getenv("API_GATEWAY", "https://genailab.tcs.in")
        self.api_key = os.getenv("API_KEY", "sk-22BGSRwNFJYu15TuXiBMog")
        self.__model = (
            "azure_ai/genailab-maas-DeepSeek-V3-0324" if model is None else model
        )
        self.__client = httpx.Client(verify=False)
        self.__llm = ChatOpenAI(
            base_url=self.gateway_url,
            model=self.__model,
            api_key=self.api_key,
            http_client=self.__client,
        )

    def invoke(self, prompt, data):
        llm_prompt = """
        PROMPT:
        {}
        DATA:
        {}
        """.format(
            prompt, data
        )
        return self.__llm.invoke(llm_prompt)
