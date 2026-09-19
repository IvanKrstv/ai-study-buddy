from fastapi import HTTPException
from openai import APIConnectionError, AsyncOpenAI

from ai_study_buddy.models.quiz_structure_models import QuizResponse
from ai_study_buddy.validators.ai_service_validator import validate_quiz

MODEL = "qwen2.5:7b-instruct" # model used for generating content

client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

SUMMARY_SYSTEM_PROMPT = """You are a study assistant that creates clear, accurate summaries of student notes.

Your task: read the notes provided by the user and produce a concise summary that captures the key concepts, definitions, and relationships between ideas — not just a shortened copy of the text.

Rules:
- Preserve technical terms, formulas, and specific names exactly as they appear in the source.
- Do not add information that is not present in the notes.
- Do not include your own opinions, commentary, or filler phrases like "This document discusses...".
- Organize the summary with short paragraphs or bullet points, whichever fits the content better.
- Keep the summary roughly 20-30% of the original length, unless the notes are very short — in that case, summarize proportionally.
- If the notes contain no meaningful academic content, respond only with: "The provided text does not contain summarizable content."
- Output the summary in the language which the notes are written in.

Output only the summary itself. Do not include headers like "Summary:" or any meta-commentary before or after it.
"""


QUIZ_SYSTEM_PROMPT = """You are a study assistant that creates clear, accurate quiz based on student notes.

Your task: read the notes provided by the user and produce an accurate quiz that questions the key concepts, definitions, and relationships between ideas.

Rules:
- Preserve technical terms, formulas, and specific names exactly as they appear in the source.
- Do not add information that is not present in the notes.
- Do not include your own opinions, commentary, or filler phrases like "This document discusses...".
- Follow strictly the requirements for number of questions and answer options from the given prompt.
- Each question has exactly one correct answer.
- Incorrect options should be plausible and related to the topic, not random or obviously wrong.
- Follow strictly the response format, presented in the request.
- If the notes contain no meaningful academic content to quiz on, return an empty questions list.
- Output the quiz in the language which the notes are written in.

Output only the quiz itself. Do not include headers like "Quiz:" or any meta-commentary before or after it.
"""


FLASHCARDS_SYSTEM_PROMPT = """
"""

async def generate_summary(notes: str) -> str:
    try:
        response = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SUMMARY_SYSTEM_PROMPT},
                {"role": "user", "content": f"Summarize the following notes:\n\n---\n{notes}\n---"}
            ],
            temperature=0.3
        )
    except APIConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Could not connect to the local AI model. Make sure Ollama is running and the model is pulled."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI generation failed: {str(e)}"
        )

    return response.choices[0].message.content


async def generate_quiz(notes: str, num_options: int = 4, num_questions: int = 5) -> QuizResponse:
    try:
        response = await client.chat.completions.parse(
            model=MODEL,
            messages=[
                {"role": "system", "content": QUIZ_SYSTEM_PROMPT},
                {"role": "user", "content": f"Generate a quiz with exactly {num_questions} questions from the following notes. "
                                            f"Each question must have exactly {num_options} answer options, with exactly one correct answer.\n\n"
                                            f"---\n{notes}\n---"}
            ],
            response_format=QuizResponse,
            temperature=0.2
        )
    except APIConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Could not connect to the local AI model. Make sure Ollama is running and the model is pulled."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI generation failed: {str(e)}"
        )

    quiz = response.choices[0].message.parsed
    validate_quiz(quiz, expected_options=num_options, expected_questions=num_questions)

    return quiz


async def generate_flashcards(notes: str, num_flashcards: int = 5):
    pass