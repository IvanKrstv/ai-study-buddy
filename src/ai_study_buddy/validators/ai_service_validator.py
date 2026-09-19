from fastapi import HTTPException

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