from loguru import logger
from qdrant_client import models

from qdrant_experimentation.day_0.setup import client


async def create_collection(collection_name: str):
    created = await client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=4, distance=models.Distance.COSINE),
    )
    logger.info(f"The collection is created?: {created}")


async def check_collection_exists(collection_name: str):
    exists = await client.collection_exists(collection_name)
    logger.info(f"Does the collection exists?: {exists}")


async def insert_points(collection_name: str, data: list[models.PointStruct]):
    inserted_results = await client.upsert(collection_name=collection_name, points=data)
    logger.info(f"Inserted points details: {inserted_results}")


async def retrieve_collection_details(collection_name: str):
    collection_details = await client.get_collection(collection_name=collection_name)
    logger.info(f"The collection details: {collection_details}")


async def query_points(collection_name: str, vector: list[int]):
    search_results = await client.query_points(
        collection_name=collection_name,
        query=vector,
        limit=1,
    )
    logger.info(f"Query results: {search_results}")


async def main():
    collection_name = "my_first_collection"
    await create_collection(collection_name=collection_name)
    await check_collection_exists(collection_name=collection_name)
    points = [
        models.PointStruct(
            id=1,
            vector=[0.1, 0.2, 0.3, 0.4],  # 4D vector
            payload={"category": "example"},  # Metadata (optional)
        ),
        models.PointStruct(
            id=2,
            vector=[0.2, 0.3, 0.4, 0.5],
            payload={"category": "demo"},
        ),
    ]
    await insert_points(collection_name=collection_name, data=points)
    await retrieve_collection_details(collection_name=collection_name)
    await query_points(collection_name=collection_name, vector=[0.08, 0.14, 0.33, 0.28])


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
