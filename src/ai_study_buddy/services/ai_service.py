from openai import OpenAI

MODEL = "qwen2.5:7b-instruct"

client = OpenAI(
    base_url="http://localhost:11434/v",
    api_key="ollama"
)


def generate_summary() -> str:
    pass


def generate_quiz() -> str:
    pass


def generate_flashcards() -> str:
    pass