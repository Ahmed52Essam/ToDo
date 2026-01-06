import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_users_me_requires_auth(client: AsyncClient):
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401


@pytest.mark.anyio
async def test_users_me_success(client: AsyncClient, auth_headers):
    # Create user headers (we assume the user needs to exist for the token to be valid if we were doing strict checks,
    # but based on auth_headers impl it just signs a token.
    # However, get_current_user implementation usually fetches from DB.
    # So we should probably Create the user first in the DB and then use its email for token.

    # Let's create a user primarily via the signup endpoint or directly in DB to be safe
    email = "me@example.com"
    password = "password"

    await client.post(
        "/api/v1/auth/signup",
        json={"email": email, "password": password},
    )

    headers = await auth_headers(email)

    response = await client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
