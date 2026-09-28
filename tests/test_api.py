"""Integration tests for the FastAPI API endpoints."""

import httpx
import pytest
import pytest_asyncio
from httpx import ASGITransport
from unittest.mock import AsyncMock, patch

from ai_study_buddy.main import app
from ai_study_buddy.models.quiz_structure_models import QuizResponse, QuizQuestion
from ai_study_buddy.models.flashcard_structure_models import FlashcardResponse, Flashcard


@pytest_asyncio.fixture
async def client():
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


# 1. No file provided → 422
class TestNoFileProvided:
    """Every upload endpoint must return 422 when no file is sent."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("endpoint", ["/extract", "/generate/summary", "/generate/quiz", "/generate/flashcards"])
    async def test_returns_422_when_no_file(self, client, endpoint):
        response = await client.post(endpoint)
        assert response.status_code == 422


# 2. Unsupported file type → 415
class TestUnsupportedFileType:
    """Uploading a .exe file should be rejected with 415."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("endpoint", ["/extract", "/generate/summary", "/generate/quiz", "/generate/flashcards"])
    @patch("ai_study_buddy.validators.file_validator.magic.from_buffer", return_value="application/x-dosexec")
    async def test_returns_415_for_exe(self, mock_magic, client, endpoint):
        response = await client.post(
            endpoint,
            files={"file": ("malware.exe", b"\x4d\x5a\x90", "application/octet-stream")},
        )
        assert response.status_code == 415


# 3. Extract endpoint — valid TXT
class TestExtractEndpoint:

    @pytest.mark.asyncio
    @patch("ai_study_buddy.validators.file_validator.magic.from_buffer", return_value="text/plain")
    async def test_extract_returns_text(self, mock_magic, client):
        response = await client.post(
            "/extract",
            files={"file": ("test.txt", b"Hello world", "text/plain")},
        )
        assert response.status_code == 200
        data = response.json()
        assert "text" in data
        assert "Hello world" in data["text"]


# 4. Summary endpoint — mock LLM
class TestSummaryEndpoint:

    @pytest.mark.asyncio
    @patch("ai_study_buddy.validators.file_validator.magic.from_buffer", return_value="text/plain")
    @patch("ai_study_buddy.main.generate_summary", new_callable=AsyncMock, return_value="Test summary")
    async def test_summary_response_structure(self, mock_gen, mock_magic, client):
        response = await client.post(
            "/generate/summary",
            files={"file": ("notes.txt", b"Some study notes", "text/plain")},
        )
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert data["summary"] == "Test summary"
        mock_gen.assert_awaited_once()


# 5. Quiz endpoint — mock LLM
class TestQuizEndpoint:

    @pytest.mark.asyncio
    @patch("ai_study_buddy.validators.file_validator.magic.from_buffer", return_value="text/plain")
    @patch(
        "ai_study_buddy.main.generate_quiz",
        new_callable=AsyncMock,
        return_value=QuizResponse(
            questions=[
                QuizQuestion(
                    question="Q?",
                    options=["A", "B", "C", "D"],
                    correct_answer_index=0,
                    explanation="Because",
                )
            ]
        ),
    )
    async def test_quiz_response_structure(self, mock_gen, mock_magic, client):
        response = await client.post(
            "/generate/quiz",
            files={"file": ("notes.txt", b"Some study notes", "text/plain")},
        )
        assert response.status_code == 200
        data = response.json()
        assert "quiz" in data

        quiz = data["quiz"]
        assert "questions" in quiz
        assert len(quiz["questions"]) == 1

        question = quiz["questions"][0]
        assert question["question"] == "Q?"
        assert question["options"] == ["A", "B", "C", "D"]
        assert question["correct_answer_index"] == 0
        assert question["explanation"] == "Because"
        mock_gen.assert_awaited_once()


# 6. Flashcards endpoint — mock LLM
class TestFlashcardsEndpoint:

    @pytest.mark.asyncio
    @patch("ai_study_buddy.validators.file_validator.magic.from_buffer", return_value="text/plain")
    @patch(
        "ai_study_buddy.main.generate_flashcards",
        new_callable=AsyncMock,
        return_value=FlashcardResponse(
            flashcards=[Flashcard(question="Q?", answer="A")]
        ),
    )
    async def test_flashcards_response_structure(self, mock_gen, mock_magic, client):
        response = await client.post(
            "/generate/flashcards",
            files={"file": ("notes.txt", b"Some study notes", "text/plain")},
        )
        assert response.status_code == 200
        data = response.json()
        assert "flashcards" in data

        flashcards = data["flashcards"]
        assert "flashcards" in flashcards
        assert len(flashcards["flashcards"]) == 1

        card = flashcards["flashcards"][0]
        assert card["question"] == "Q?"
        assert card["answer"] == "A"
        mock_gen.assert_awaited_once()


# 7. Static files — GET / serves HTML
class TestStaticFiles:

    @pytest.mark.asyncio
    async def test_root_returns_html(self, client):
        response = await client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
