from fastapi import FastAPI, UploadFile

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