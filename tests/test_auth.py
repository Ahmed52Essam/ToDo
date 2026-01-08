import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_signup(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/signup",
        json={"email": "newuser@example.com", "password": "strongpassword"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert "hashed_password" not in data  # Should not expose password


@pytest.mark.anyio
async def test_signup_existing_email(client: AsyncClient):
    # Create first user
    await client.post(
        "/api/v1/auth/signup",
        json={"email": "duplicate@example.com", "password": "strongpassword"},
    )
    # Try to create same user again
    response = await client.post(
        "/api/v1/auth/signup",
        json={"email": "duplicate@example.com", "password": "anotherpassword"},
    )
    assert response.status_code == 409


@pytest.mark.anyio
async def test_login(client: AsyncClient):
    # Signup first
    response = await client.post(
        "/api/v1/auth/signup",
        json={"email": "loginuser@example.com", "password": "strongpassword"},
    )
    # assert response.status_code == 200

    # Login
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "loginuser@example.com", "password": "strongpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.anyio
async def test_login_wrong_password(client: AsyncClient):
    # Signup
    await client.post(
        "/api/v1/auth/signup",
        json={"email": "wrongpass@example.com", "password": "strongpassword"},
    )

    # Login with wrong password
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "wrongpass@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
