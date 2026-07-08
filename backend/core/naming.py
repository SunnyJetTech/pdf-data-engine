import re
import uuid

def generate_collection_name(filename: str) -> str:
    safe = re.sub(
        r"[^a-zA-Z0-9_]",
        "_",
        filename,
    )

    return f"{safe}_{uuid.uuid4().hex[:8]}"