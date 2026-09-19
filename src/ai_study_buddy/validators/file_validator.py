import magic
from fastapi import HTTPException


class FileValidator:
    _MAX_FILE_SIZE_MB = 10
    _MAX_FILE_SIZE_BYTES = _MAX_FILE_SIZE_MB * 1024 * 1024
    _ALLOWED_CONTENT_TYPES = {
        'pdf': {'application/pdf'},
        'docx': {'application/vnd.openxmlformats-officedocument.wordprocessingml.document'},
        'txt': {'text/plain'},
    }


    def validate_file_size(self, file_size: int) -> None:
        if file_size > self._MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum allowed size is {self._MAX_FILE_SIZE_MB} MB."
            )


    def validate_extension(self, file_extension: str) -> None:
        if file_extension not in self._ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=415,
                detail=self._allowed_types_message
            )

    def validate_content_matches_extension(self, file_extension: str, content: bytes) -> None:
        detected_type = magic.from_buffer(content, mime=True)
        allowed_types = self._ALLOWED_CONTENT_TYPES[file_extension]

        if detected_type not in allowed_types:
            raise HTTPException(
                status_code=415,
                detail=f"File content doesn't match a .{file_extension} file (detected: '{detected_type}')."
            )

    @staticmethod
    def empty_text_content_check(text: str | list[str], error_message: str) -> None:
        combined = text if isinstance(text, str) else ''.join(text)
        if not combined.strip():
            raise HTTPException(
                status_code=422,
                detail=error_message
            )


    @property
    def _allowed_types_message(self):
        return (f"Not supported file extension. Upload a file with extension: "
                f"{', '.join([f'.{ext}' for ext in self._ALLOWED_CONTENT_TYPES.keys()])}.")