import logging
from contextlib import contextmanager

from fastapi import HTTPException
from openai import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    ContentFilterFinishReasonError,
    LengthFinishReasonError,
    RateLimitError, InternalServerError,
)
from pydantic import ValidationError

logger = logging.getLogger(__name__)


@contextmanager
def translate_llm_errors():
    """Turn errors from the LLM client into HTTPExceptions with user-friendly messages."""

    try:
        yield
    except RateLimitError as e:
        logger.warning(f"LLM rate limit hit: {e}")
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again in a minute.",
        ) from e
    except APITimeoutError as e:
        logger.error(f"LLM request timed out: {e}")
        raise HTTPException(
            status_code=504,
            detail="The AI model took too long to respond. Please try again.",
        ) from e
    except APIConnectionError as e:
        logger.error(f"Could not connect to the LLM: {e}")
        raise HTTPException(
            status_code=503,
            detail="Could not connect to the AI model.",
        ) from e
    except (LengthFinishReasonError, ContentFilterFinishReasonError, ValidationError) as e:
        logger.error(f"Invalid or incomplete LLM output: {e}")
        raise HTTPException(
            status_code=502,
            detail="The AI returned an invalid response. Please try again.",
        ) from e
    except AuthenticationError as e:
        logger.error(f"LLM authentication failed, check the API key: {e}")
        raise HTTPException(
            status_code=500,
            detail="AI generation failed. Please try again later.",
        ) from e
    except InternalServerError as e:
        logger.error(f"LLM provider returned a server error: {e}")
        raise HTTPException(
            status_code=503,
            detail="The AI model is temporarily overloaded. Please try again in a moment.",
        ) from e
    except Exception as e:
        logger.exception("Unexpected error during LLM call")
        raise HTTPException(
            status_code=500,
            detail="AI generation failed. Please try again later.",
        ) from e