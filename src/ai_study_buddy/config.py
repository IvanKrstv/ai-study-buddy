from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    llm_base_url: str = 'http://localhost:11434/v1'
    llm_api_key: str = 'ollama'
    llm_model: str = 'qwen2.5:7b-instruct'
    llm_summary_temperature: float | None = None
    llm_structured_temperature: float | None = None


settings = Settings()