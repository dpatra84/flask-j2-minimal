import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA
import httpx
from app import app


class LLMService:
    def __init__(self, llm_model=None, embedding_model=None):
        self.__gateway_url = os.getenv("API_GATEWAY", "https://genailab.tcs.in")
        self.__api_key = os.getenv("API_KEY")
        self.__llm_model = (
            "azure_ai/genailab-maas-DeepSeek-V3-0324"
            if llm_model is None
            else llm_model
        )
        self.__embedding_model = (
            "azure_ai/genailab-maas-text-embedding-3-large"
            if embedding_model is None
            else embedding_model
        )
        self.__client = httpx.Client(verify=False)
        self.llm = ChatOpenAI(
            base_url=self.__gateway_url,
            model=self.__llm_model,
            api_key=self.__api_key,
            http_client=self.__client,
        )
        self.embedding = OpenAIEmbeddings(
            base_url=self.__gateway_url,
            model=self.__embedding_model,
            api_key=self.__api_key,
            http_client=self.__client,
        )
        self.vectordb = None

    def doc_index(self, raw_text):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        chunks = text_splitter.split_text(raw_text)
        self.vectordb = Chroma.from_texts(
            chunks,
            self.embedding,
            persist_directory=app.config["VECTOR_STORAGE_FOLDER"],
        )
        self.vectordb.persist()

    def build_rag(self):
        self.retriever = self.vectordb.as_retriever(
            search_type="similarity", search_kwargs={"k": 5}
        )
        self.rag_chain = RetrievalQA.from_chain_type(
            llm=self.llm, retriever=self.retriever, return_source_documents=True
        )

    def invoke(self, prompt, data):
        self.doc_index(data)
        self.build_rag()
        return self.rag_chain.invoke(prompt)
