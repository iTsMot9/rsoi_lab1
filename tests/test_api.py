import pytest
from httpx import AsyncClient
from app.main import app

BASE_URL = "http://test"


@pytest.mark.asyncio
async def test_create_person():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.post("/persons", json={
            "name": "Alex",
            "age": 20,
            "address": "Moscow",
            "work": "cringineer"
        })
        assert response.status_code == 201
        assert "Location" in response.headers
        location = response.headers["Location"]
        assert location.startswith("/api/v1/persons/")


@pytest.mark.asyncio
async def test_get_person():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        create_resp = await ac.post("/persons", json={
            "name": "Bob",
            "age": 25,
            "address": "Dubai",
            "work": "sheikh"
        })
        person_id = create_resp.headers["Location"].split("/")[-1]

        response = await ac.get(f"/persons/{person_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Bob"
        assert data["age"] == 25
        assert data["address"] == "Dubai"
        assert data["work"] == "sheikh"
        assert data["id"] == int(person_id)


@pytest.mark.asyncio
async def test_get_all_persons():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        await ac.post("/persons", json={"name": "Rob", "age": 40, "address": "Italy", "work": "mafia"})
        await ac.post("/persons", json={"name": "Oleg", "age": 45, "address": "Italy", "work": "don"})

        response = await ac.get("/persons")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        names = {p["name"] for p in data}
        assert "Rob" in names
        assert "Oleg" in names


@pytest.mark.asyncio
async def test_update_person():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        create_resp = await ac.post("/persons", json={
            "name": "Walli",
            "age": 100,
            "address": "Earth",
            "work": "garbager"
        })
        person_id = create_resp.headers["Location"].split("/")[-1]

        response = await ac.patch(f"/persons/{person_id}", json={
            "name": "Walli-E",
            "age": 101
        })
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Walli-E"
        assert data["age"] == 101
        assert data["address"] == "Earth"      
        assert data["work"] == "garbager"      


@pytest.mark.asyncio
async def test_delete_person():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        create_resp = await ac.post("/persons", json={
            "name": "Chappi",
            "age": 15,
            "address": "gheto",
            "work": "robber"
        })
        person_id = create_resp.headers["Location"].split("/")[-1]

        delete_resp = await ac.delete(f"/persons/{person_id}")
        assert delete_resp.status_code == 204

        get_resp = await ac.get(f"/persons/{person_id}")
        assert get_resp.status_code == 404
