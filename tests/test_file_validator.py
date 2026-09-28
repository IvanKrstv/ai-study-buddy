import pytest
from unittest.mock import patch
from fastapi import HTTPException

from ai_study_buddy.validators.file_validator import FileValidator


@pytest.fixture
def validator():
    return FileValidator()


class TestValidateFileSize:
    def test_none_size_raises_422(self, validator):
        with pytest.raises(HTTPException) as exc:
            validator.validate_file_size(None)
        assert exc.value.status_code == 422

    def test_over_limit_raises_413(self, validator):
        over = FileValidator._MAX_FILE_SIZE_BYTES + 1
        with pytest.raises(HTTPException) as exc:
            validator.validate_file_size(over)
        assert exc.value.status_code == 413

    def test_at_limit_passes(self, validator):
        validator.validate_file_size(FileValidator._MAX_FILE_SIZE_BYTES)  # no exception

    def test_under_limit_passes(self, validator):
        validator.validate_file_size(1024)  # no exception

    def test_zero_size_passes(self, validator):
        validator.validate_file_size(0)  # no exception



class TestValidateExtension:
    @pytest.mark.parametrize("ext", ["pdf", "docx", "txt"])
    def test_valid_extension_passes(self, validator, ext):
        validator.validate_extension(ext)  # no exception

    @pytest.mark.parametrize("ext", ["exe", "py", "jpg", "png", "html", "csv", ""])
    def test_invalid_extension_raises_415(self, validator, ext):
        with pytest.raises(HTTPException) as exc:
            validator.validate_extension(ext)
        assert exc.value.status_code == 415



class TestValidateContentMatchesExtension:
    @patch("ai_study_buddy.validators.file_validator.magic.from_buffer")
    def test_matching_mime_passes(self, mock_magic, validator):
        mock_magic.return_value = "application/pdf"
        validator.validate_content_matches_extension("pdf", b"fake pdf bytes")

    @patch("ai_study_buddy.validators.file_validator.magic.from_buffer")
    def test_mismatching_mime_raises_415(self, mock_magic, validator):
        mock_magic.return_value = "text/plain"
        with pytest.raises(HTTPException) as exc:
            validator.validate_content_matches_extension("pdf", b"not a pdf")
        assert exc.value.status_code == 415
        assert "text/plain" in exc.value.detail

    @patch("ai_study_buddy.validators.file_validator.magic.from_buffer")
    def test_txt_content_matches(self, mock_magic, validator):
        mock_magic.return_value = "text/plain"
        validator.validate_content_matches_extension("txt", b"hello")

    @patch("ai_study_buddy.validators.file_validator.magic.from_buffer")
    def test_docx_content_matches(self, mock_magic, validator):
        mock_magic.return_value = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        validator.validate_content_matches_extension("docx", b"fake docx")



class TestEmptyTextContentCheck:
    def test_empty_string_raises_422(self, validator):
        with pytest.raises(HTTPException) as exc:
            validator.empty_text_content_check("", "empty")
        assert exc.value.status_code == 422

    def test_whitespace_only_string_raises_422(self, validator):
        with pytest.raises(HTTPException) as exc:
            validator.empty_text_content_check("   \n\t  ", "empty")
        assert exc.value.status_code == 422

    def test_empty_list_raises_422(self, validator):
        with pytest.raises(HTTPException) as exc:
            validator.empty_text_content_check([], "empty")
        assert exc.value.status_code == 422

    def test_whitespace_only_list_raises_422(self, validator):
        with pytest.raises(HTTPException) as exc:
            validator.empty_text_content_check(["  ", "\n", "\t"], "empty")
        assert exc.value.status_code == 422

    def test_valid_string_passes(self, validator):
        validator.empty_text_content_check("some real content", "empty")

    def test_valid_list_passes(self, validator):
        validator.empty_text_content_check(["page 1", "page 2"], "empty")

    def test_custom_error_message_used(self, validator):
        with pytest.raises(HTTPException) as exc:
            validator.empty_text_content_check("", "Custom error message")
        assert exc.value.detail == "Custom error message"



class TestValidateTextLength:
    def test_within_limit_passes(self, validator):
        validator.validate_text_length("a" * 100_000)  # exactly at limit

    def test_over_limit_raises_413(self, validator):
        with pytest.raises(HTTPException) as exc:
            validator.validate_text_length("a" * 100_001)
        assert exc.value.status_code == 413

    def test_short_text_passes(self, validator):
        validator.validate_text_length("short text")

    def test_empty_text_passes(self, validator):
        validator.validate_text_length("")