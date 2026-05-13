from loguru import logger
from qdrant_client import models

from qdrant_experimentation.day_0.setup import client


async def create_collection(collection_name: str):
    created = await client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=4, distance=models.Distance.COSINE),
    )

    logger.info(f"The collection is created?: {created}")
    payload_index_created = await client.create_payload_index(
        collection_name=collection_name,
        field_name="category",
        field_schema=models.PayloadSchemaType.KEYWORD,
    )

    logger.info(f"The payload index is created?: {payload_index_created}")


async def upsert_points(collection_name: str):
    points = [
        models.PointStruct(
            id=1,
            vector=[0.9, 0.1, 0.1, 0.8],  # High affordability, high innovation
            payload={
                "name": "Budget Smartphone",
                "category": "electronics",
                "price": 299,
            },
        ),
        models.PointStruct(
            id=2,
            vector=[0.2, 0.9, 0.8, 0.5],  # High quality, high popularity
            payload={"name": "Bestselling Novel", "category": "books", "price": 19},
        ),
        models.PointStruct(
            id=3,
            vector=[
                0.8,
                0.3,
                0.2,
                0.9,
            ],  # High affordability, high innovation (similar to ID 1)
            payload={"name": "Smart Home Hub", "category": "electronics", "price": 89},
        ),
        models.PointStruct(
            id=4,
            vector=[0.7, 0.4, 0.3, 0.8],
            payload={"name": "Laptop", "category": "electronics", "price": 1000},
        ),
        models.PointStruct(
            id=5,
            vector=[0.7, 0.4, 0.3, 0.8],
            payload={"name": "Laptop", "category": "electronics", "price": 1000},
        ),
    ]

    response = await client.upsert(
        collection_name=collection_name,
        points=points,
    )

    logger.info(f"The points are upserted?: {response}")


async def simple_query_points(
    collection_name: str,
    query_vector: list[float],
    limit: int,
):
    query_result = await client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=limit,
    )

    logger.info(f"The search result is: {query_result}")


async def filter_query_points(
    collection_name: str,
    query_vector: list[float],
    limit: int,
):
    filter_query_result = await client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=limit,
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="category",
                    match=models.MatchValue(value="electronics"),
                ),
            ],
        ),
    )

    logger.info(f"The filter search result is: {filter_query_result}")


async def delete_collection(collection_name: str):
    response = await client.delete_collection(collection_name=collection_name)
    logger.info(f"The collection is deleted?: {response}")


async def main():
    collection_name = "day0_first_system"
    await create_collection(collection_name=collection_name)
    await upsert_points(collection_name=collection_name)
    query_vector = [0.85, 0.2, 0.1, 0.9]
    await simple_query_points(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=1,
    )
    await filter_query_points(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=1,
    )
    # await delete_collection(collection_name=collection_name)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
