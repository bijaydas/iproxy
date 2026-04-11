from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from app.core import settings
from app.utils.general import require_llm


class LLMService:
    llm: ChatOpenAI

    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            api_key=settings.OPENAI_API_KEY,
        )

    @require_llm
    def classify_query_source(self, query: str):
        prompt = PromptTemplate.from_template(
            f"Classify this query as either {settings.COLLECTION_RESUME} or {settings.COLLECTION_JOB_DESCRIPTION}.\n"
            f"Reply with only one word: {settings.COLLECTION_RESUME} or {settings.COLLECTION_JOB_DESCRIPTION}.\n\n"
            "Query: {query}"
        )

        result = self.llm.invoke(prompt.format(query=query))

        return result.content.strip().lower()

    @require_llm
    def answer_query(self, user_query: str, document_results: list):
        context = "\n\n".join([
            doc.page_content for doc in document_results
        ])

        prompt = PromptTemplate.from_template(
            "You are a helpful assistant. Dont add words like \"mentioned in context etc.\""
            "Use the following context to answer the question.\n\n"
            f"Context: {context}\n\n"
            f"User query: {user_query}\n\n"
            "Answer:"
        )
        result = self.llm.invoke(prompt.format(context=context, user_query=user_query))

        return result.content.strip()

    @require_llm
    def resume_improvements(self, resume_content: str, job_description_content: str):
        prompt_template = PromptTemplate.from_template("""
You are an expert resume coach and ATS specialist.

You will be given a candidate's resume and a job description.
Your task is to analyze the resume against the job description and provide specific, actionable improvements.

---

## Job Description
{job_description_content}

---

## Candidate Resume
{resume_content}

---

## Your Task

Analyze the resume against the job description and provide:

1. **Match Score** — Give a percentage score (0-100) of how well the resume matches the JD.

2. **Missing Keywords** — List important keywords/skills from the JD that are missing in the resume.

3. **Weak Sections** — Identify resume sections that are weak or vague relative to what the JD expects.

4. **Suggested Improvements** — For each weak point, give a concrete rewritten version.

5. **Summary Rewrite** — Rewrite the resume summary to better align with the JD.

6. **Overall Advice** — 2-3 lines of general strategic advice.

Be specific, direct, and actionable. No generic advice.
        """)

        prompt = prompt_template.format(job_description_content=job_description_content, resume_content=resume_content)

        result = self.llm.invoke(prompt)

        return result.content.strip()
