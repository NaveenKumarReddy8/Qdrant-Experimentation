from os import environ
from pathlib import Path

from dotenv import load_dotenv
from qdrant_client import AsyncQdrantClient

env_file_path = Path(__file__).parent.parent.parent.parent / ".env"

load_dotenv(dotenv_path=env_file_path)

client = AsyncQdrantClient(
    url=environ["QDRANT_URL"],
    api_key=environ["QDRANT_API_KEY"],
)
