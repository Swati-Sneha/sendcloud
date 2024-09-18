import pytest
from fastapi.testclient import TestClient
from asgi_lifespan import LifespanManager
from collections.abc import AsyncIterable
from httpx import AsyncClient
from typing import AsyncGenerator
from app import app


# @pytest.fixture(scope="function")
# async def async_client()-> AsyncIterable[AsyncClient]:
#     async with LifespanManager(app):   # Wrapping the app with a lifespan asgi
#         async with AsyncClient(app=app, base_url="http://test") as c:
#             yield c
            
            
# @pytest.fixture
# async def async_client() -> AsyncClient:
#     async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
#         yield client
        
@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test/timer") as client:
        yield client

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(scope="session") # to scope as session the anyio backend
def anyio_backend() -> str:
    return "asyncio"