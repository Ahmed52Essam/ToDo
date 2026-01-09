import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_task_ownership_isolation(client: AsyncClient, auth_headers):
    # User A
    email_a = "user_a@example.com"
    await client.post(
        "/api/v1/auth/signup",
        json={"email": email_a, "password": "password"},
    )
    headers_a = await auth_headers(email_a)

    # User A creates a task
    res = await client.post(
        "/api/v1/tasks/",
        headers=headers_a,
        json={"title": "Task A"},
    )
    assert res.status_code == 201
    task_id = res.json()["id"]

    # User B
    email_b = "user_b@example.com"
    await client.post(
        "/api/v1/auth/signup",
        json={"email": email_b, "password": "password"},
    )
    headers_b = await auth_headers(email_b)

    # User B tries to read User A's task
    res = await client.get(f"/api/v1/tasks/{task_id}", headers=headers_b)
    assert res.status_code == 404

    # User B tries to update User A's task
    res = await client.patch(
        f"/api/v1/tasks/{task_id}", headers=headers_b, json={"title": "Hacked Title"}
    )
    assert res.status_code == 404

    # User B tries to delete User A's task
    res = await client.delete(f"/api/v1/tasks/{task_id}", headers=headers_b)
    assert res.status_code == 404

    # Ensure User A can still access it
    res = await client.get(f"/api/v1/tasks/{task_id}", headers=headers_a)
    assert res.status_code == 200


@pytest.mark.anyio
async def test_create_task_validation(client: AsyncClient, auth_headers):
    # Setup user
    email = "val@example.com"
    await client.post(
        "/api/v1/auth/signup",
        json={"email": email, "password": "password"},
    )
    headers = await auth_headers(email)

    # Create valid task
    res = await client.post(
        "/api/v1/tasks/",
        headers=headers,
        json={"title": "Valid Task"},
    )
    assert res.status_code == 201
    task_id = res.json()["id"]

    # Create with empty title
    res = await client.post(
        "/api/v1/tasks/",
        headers=headers,
        json={"title": ""},
    )
    assert res.status_code == 422

    # Patch with empty title
    res = await client.patch(
        f"/api/v1/tasks/{task_id}",
        headers=headers,
        json={"title": ""},
    )
    assert res.status_code == 422


@pytest.mark.anyio
async def test_search_and_filter_tasks(client: AsyncClient, auth_headers):
    email = "filter@example.com"
    await client.post(
        "/api/v1/auth/signup",
        json={"email": email, "password": "password"},
    )
    headers = await auth_headers(email)

    # Create 3 tasks
    # 1. Buy Groceries (Pending)
    await client.post(
        "/api/v1/tasks/", headers=headers, json={"title": "Buy Groceries"}
    )
    # 2. Buy Milk (Completed) - We need to patch this one to be completed
    res = await client.post(
        "/api/v1/tasks/", headers=headers, json={"title": "Buy Milk"}
    )
    task_id = res.json()["id"]
    await client.patch(
        f"/api/v1/tasks/{task_id}", headers=headers, json={"completed": True}
    )
    # 3. Do Homework (Pending)
    await client.post("/api/v1/tasks/", headers=headers, json={"title": "Do Homework"})

    # Test 1: Filter by Completed=True (Should get "Buy Milk")
    res = await client.get("/api/v1/tasks/?completed=true", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["title"] == "Buy Milk"

    # Test 2: Search for "buy" (Should get "Buy Groceries" and "Buy Milk")
    res = await client.get("/api/v1/tasks/?search=buy", headers=headers)
    assert len(res.json()) == 2

    # Test 3: Pagination (Limit 1)
    res = await client.get("/api/v1/tasks/?limit=1", headers=headers)
    assert len(res.json()) == 1
