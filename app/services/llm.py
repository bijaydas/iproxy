from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from app.core import settings


class LLMService:
    llm: ChatOpenAI
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            api_key=settings.OPENAI_API_KEY,
        )

    def classify_query_source(self, query: str):
        prompt = PromptTemplate.from_template(
            f"Classify this query as either {settings.COLLECTION_RESUME} or {settings.COLLECTION_JOB_DESCRIPTION}.\n"
            f"Reply with only one word: {settings.COLLECTION_RESUME} or {settings.COLLECTION_JOB_DESCRIPTION}.\n\n"
            "Query: {query}"
        )

        result = self.llm.invoke(prompt.format(query=query))

        return result.content.strip().lower()

    def answer_query(self, user_query: str, document_results: list):
        context = "\n\n".join([
            doc.page_content for doc in document_results
        ])

        prompt = PromptTemplate.from_template(
            "You are a helpful assistant. Dont add words like \"mentioned in context etc.\" Use the following context to answer the question.\n\n"
            f"Context: {context}\n\n"
            f"User query: {user_query}\n\n"
            "Answer:"
        )
        result = self.llm.invoke(prompt.format(context=context, user_query=user_query))

        return result.content.strip()