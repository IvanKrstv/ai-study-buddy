import uvicorn


def main() -> None:
    uvicorn.run("ai_study_buddy.main:app", host="127.0.0.1", port=8000)
