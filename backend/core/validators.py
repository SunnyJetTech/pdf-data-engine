from fastapi import UploadFile

async def validate_file_size(file: UploadFile, max_size_mb: int,):
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)

    max_bytes = max_size_mb * 1024 * 1024

    if size > max_bytes:
        raise ValueError(
            f"File exceeds maximum size of {max_size_mb} MB"
        )