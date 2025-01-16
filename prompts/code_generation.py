from langchain.prompts import PromptTemplate

CODE_GENERATION_PROMPT = PromptTemplate(
    input_variables=["task_description"],
    template="Напиши код на Python для следующей задачи: {task_description}",
)