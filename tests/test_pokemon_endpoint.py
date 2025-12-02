from fastapi.testclient import TestClient


def test_create_pokemon_record_pikachu(client: TestClient):
    response = client.post(
        "/api/v1/pokemon/",
        json={"pokemon_name": "pikachu"},
    )

    assert response.status_code == 201

    data = response.json()
    assert data["pokemon_name"] == "pikachu"
    assert data["pokedex_id"] == 25

    assert isinstance(data["total_base_stats"], int)
    assert isinstance(data["power_index"], (int, float))
    assert data["tier"] in {"S", "A", "B", "C"}


def test_create_pokemon_record_not_found(client: TestClient):
    response = client.post(
        "/api/v1/pokemon/",
        json={"pokemon_name": "this-is-not-a-real-pokemon"},
    )

    assert response.status_code == 404
    body = response.json()
    assert "not found" in body["detail"].lower()
