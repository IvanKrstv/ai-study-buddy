from fastapi import HTTPException

from ai_study_buddy.models.flashcard_structure_models import FlashcardResponse
from ai_study_buddy.models.quiz_structure_models import QuizResponse


def validate_quiz(quiz: QuizResponse, expected_options: int, expected_questions: int) -> None:
    if not quiz.questions:
        raise HTTPException(
            status_code=422,
            detail="The notes don't contain enough meaningful content to generate a quiz."
        )

    if len(quiz.questions) != expected_questions:
        raise HTTPException(
            status_code=502,
            detail=f"AI returned {len(quiz.questions)} questions, expected {expected_questions}."
        )

    for i, question in enumerate(quiz.questions):
        if len(question.options) != expected_options:
            raise HTTPException(
                status_code=502,
                detail=f"Question {i + 1} has {len(question.options)} options, expected {expected_options}."
            )
        if not (0 <= question.correct_answer_index < len(question.options)):
            raise HTTPException(
                status_code=502,
                detail=f"Question {i + 1} has an invalid correct_answer_index."
            )


def validate_flashcards(flashcards_response: FlashcardResponse, expected_flashcards:int) -> None:
    if not flashcards_response.flashcards:
        raise HTTPException(
            status_code=422,
            detail="The notes don't contain enough meaningful content to generate flashcards."
        )

    min_acceptable = max(1, round(expected_flashcards * 0.7))  # accepts at least 70% of the expected number
    max_acceptable = round(expected_flashcards * 1.5)  # accepts at most 150% of the expected number

    actual = len(flashcards_response.flashcards)

    if actual < min_acceptable:
        raise HTTPException(
            status_code=502,
            detail=f"AI returned only {actual} flashcards, expected around {expected_flashcards}."
        )

    if actual > max_acceptable:
        raise HTTPException(
            status_code=502,
            detail=f"AI returned {actual} flashcards, expected around {expected_flashcards}."
        )