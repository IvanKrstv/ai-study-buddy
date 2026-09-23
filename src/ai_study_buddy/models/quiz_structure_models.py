from pydantic import BaseModel


class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    correct_answer_index: int
    explanation: str


class QuizResponse(BaseModel):
    questions: list[QuizQuestion]