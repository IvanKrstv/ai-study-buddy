from fastapi import HTTPException
from openai import APIConnectionError, AsyncOpenAI

MODEL = "qwen2.5:7b-instruct"

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

Output only the summary itself. Do not include headers like "Summary:" or any meta-commentary before or after it."""


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


def generate_quiz(notes: str, num_questions: int = 10):
    pass


def generate_flashcards(notes: str, num_flashcards: int = 5):
    pass