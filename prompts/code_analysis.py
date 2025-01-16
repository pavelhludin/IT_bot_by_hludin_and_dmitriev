from langchain.prompts import PromptTemplate

CODE_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["code"],
    template="Проанализируй следующий код и предложи улучшения:\n{code}",
)