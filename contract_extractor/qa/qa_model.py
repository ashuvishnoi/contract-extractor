from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class CUADQAModel:
    """
    LLM-based QA model using LangChain + OpenAI.
    Designed for contract clause extraction.
    """

    def __init__(self, model_name="gpt-4"):
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0,
            openai_api_key=OPENAI_API_KEY
        )

        self.prompt = ChatPromptTemplate.from_template("""
You are a precise legal contract analysis assistant.
Answer the question strictly based on the contract text below.
Return the response strictly based on given output_type
The response should also contain confidence score and page number of the source. If the answer is not present, return empty string and confidence score should be 0.
confidence score should be between 0 and 1, where 1 means the answer is explicitly stated in the contract and 0 means the answer is not found in the contract.
Example: if output_type is date, you should just answer in date format, nothing else. (Obviously if date is part of answer)
The final response must be like: {{'answer': '', 'page_number': '', 'confidence_score': '}}


Contract Text:
{context}

Question:
{question}

Output Type:
{output_type}

Answer concisely:
""")

        self.chain = self.prompt | self.llm | StrOutputParser()

    def predict(self, question, docs, output_type):
        """
        question: str
        docs: list of LangChain Document objects
        """

        context = "\n\n".join(
            [
                f"Page {doc['page_number']}:\n{doc['content'].strip()}"
                for doc in docs
            ]
        )
        return self.chain.invoke({
            "context": context,
            "question": question,
            "output_type": output_type
        })
