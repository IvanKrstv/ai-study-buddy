from fastapi import FastAPI, UploadFile

from ai_study_buddy.services.ai_service import generate_summary, generate_quiz, generate_flashcards
from ai_study_buddy.services.file_service import ExtractFile

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post('/extract')
async def extract_text(file: UploadFile):
    extractor = ExtractFile(file)
    text = await extractor.extract_text()
    return {
        'text': text
    }


@app.post('/generate/summary')
async def generate_ai_summary(file: UploadFile):
    extractor = ExtractFile(file)
    notes = await extractor.extract_text()

    summary = await generate_summary(notes)

    return {
        'summary': summary
    }


@app.post('/generate/quiz')
async def generate_ai_quiz(file: UploadFile):
    extractor = ExtractFile(file)
    notes = await extractor.extract_text()

    quiz = await generate_quiz(notes, num_options=4, num_questions=5)

    return {
        'quiz': quiz
    }


@app.post('/generate/flashcards')
async def generate_ai_flashcards(file: UploadFile):
    extractor = ExtractFile(file)
    notes = await extractor.extract_text()

    flashcards = await generate_flashcards(notes, num_flashcards=5)

    return {
        'flashcards': flashcards
    }