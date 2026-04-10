from pathlib import Path
from typing import List

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.logger import logger
from app.core.settings import settings


class ChromaDBService:
    embeddings: OpenAIEmbeddings = None

    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            api_key=settings.OPENAI_API_KEY
        )

    def get_collection(self, name: str) -> Chroma:
        return Chroma(
            persist_directory=settings.CHROMA_DB_PATH,
            embedding_function=self.embeddings,
            collection_name=name,
            create_collection_if_not_exists=True,
        )

    @classmethod
    def _split_text(cls, content: str) -> List[str]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=30,
        )
        return splitter.split_text(content)

    @classmethod
    def _convert_to_documents(cls, texts: List[str], user_id: str, source: str, type: str) -> List[Document]:
        documents = []

        for text in texts:
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "user_id": user_id,
                        "source": source,
                        "type": type,
                    }
                )
            )

        return documents

    @classmethod
    def _get_ids(cls, texts: List[str], user_id: str) -> List[str]:
        return [f"{user_id}_{str(x)}" for x in range(len(texts))]

    def embedd_resume(self, resume_path: str, user_id: str):
        file_path = Path(resume_path)

        if not file_path.exists():
            logger.error(f"Resume file {resume_path} does not exist")
            raise FileNotFoundError(f"Resume file not found: {resume_path}")

        with open(file_path, "r", encoding="utf8") as f:
            content = f.read()

            if len(content) < 100:
                logger.error(f"Resume file {resume_path} is too short")
                raise Exception("Resume file too short")

        texts = self._split_text(content)

        ids = self._get_ids(texts, user_id)
        documents = self._convert_to_documents(texts, user_id, str(file_path), "resume")

        collection = self.get_collection(settings.COLLECTION_RESUME)

        collection.add_documents(documents, ids=ids)

        return True

    def embedd_job_description(self, job_description_path: str, user_id: str):
        file_path = Path(job_description_path)

        if not file_path.exists():
            logger.error(f"job_description_path file {job_description_path} does not exist")
            raise FileNotFoundError(f"job_description_path file not found: {job_description_path}")

        with open(file_path, "r", encoding="utf8") as f:
            content = f.read()

            if len(content) < 100:
                logger.error(f"job_description_path file {job_description_path} is too short")
                raise Exception("job_description_path file too short")

        texts = self._split_text(content)

        ids = self._get_ids(texts, user_id)
        documents = self._convert_to_documents(texts, user_id, str(file_path), "job_description")

        collection = self.get_collection(settings.COLLECTION_JOB_DESCRIPTION)

        collection.add_documents(documents, ids=ids)

        return True
