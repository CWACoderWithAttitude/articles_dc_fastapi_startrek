import json
from typing import Any

from httpx import Response
from main import app
from fastapi.testclient import TestClient
from fastapi import status
from test_utils.mock_ships import _create_mock_ships
from test_utils.fixtures import session_fixture, client_fixture


def test_get_info(client: TestClient) -> None:
    """
    Test the / endpoint.
    """
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-type'] == 'application/json'
    response_json = response.json()
    assert response_json != None
    assert response_json['message'] == 'Welcome to the FastAPI application!'


def test_create_ship(client: TestClient) -> None:
    """
    Test the /ships/ endpoint.
    """
    response = client.post("/ships/", json={
        "name": "Test Ship",
        "classification": "Test Classification",
        "sign": "Test Sign",
        "speed": "Test Speed",
        "captain": "Test Captain",
        "comment": "Test Comment",
        "url": "http://example.com"
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.headers['content-type'] == 'application/json'
    response_json = response.json()
    assert response_json != None
    assert response_json['name'] == 'Test Ship'
    assert response_json['classification'] == 'Test Classification'
    assert response_json['sign'] == 'Test Sign'
    assert response_json['speed'] == 'Test Speed'
    assert response_json['id'] >= 1


def test_get_all_ships(client: TestClient) -> None:
    """
    Test the /ships/ endpoint.
    """
    _create_mock_ships(client, 5)
    response = client.get("/ships/")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-type'] == 'application/json'
    response_json = response.json()
    assert response_json != None
    assert len(response_json) == 5


def test_ship_by_non_existing_id(client: TestClient) -> None:
    """
    Test the /ships/{ship_id} endpoint.
    """
    _create_mock_ships(client, 5)
    response: Response = client.get("/ships/6")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_ship_by_existing_id(client: TestClient) -> None:
    """
    Test the /ships/{ship_id} endpoint.
    """
    _create_mock_ships(client, 3)
    id_to_query = 3
    response = client.get(f"/ships/{id_to_query}")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-type'] == 'application/json'
    response_json = response.json()
    assert response_json != None
    assert response_json['id'] == id_to_query
    assert response_json['name'] == f'Test Ship {id_to_query-1}'
    assert response_json['classification'] == f'Test Classification {id_to_query-1}'
    assert response_json['sign'] == f'Test Sign {id_to_query-1}'


def test_get_ships_limit(client: TestClient) -> None:
    """
    Test the /ships/ endpoint and limit the result count.
    """
    _create_mock_ships(client, 5)
    response = client.get("/ships/?limit=2")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-type'] == 'application/json'
    response_json = response.json()
    assert response_json != None
    assert len(response_json) == 2


def test_update_existing_ship(client: TestClient) -> None:
    """
    Test the /ships/ endpoint.
    """
    response = client.post("/ships/", json={
        "name": "Test Ship",
        "classification": "Test Classification",
        "sign": "Test Sign",
        "speed": "Test Speed",
        "captain": "Test Captain",
        "comment": "Test Comment",
        "url": "http://example.com"
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.headers['content-type'] == 'application/json'
    response_json = response.json()
    assert response_json != None
    ship_id = response_json['id']
    response: Response = client.put(f"/ships/{ship_id}", json={
        "name": "Updated Ship",
        "classification": "Updated Classification",
        "sign": "Updated Sign",
        "speed": "Updated Speed",
        "captain": "Updated Captain",
        "comment": "Updated Comment",
        "url": "http://example.com/updated"
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-type'] == 'application/json'
    response_json = response.json()
    assert response_json != None
    assert response_json['name'] == 'Updated Ship'


def test_update_non_existing_ship(client: TestClient) -> None:
    """
    Test the /ships/ endpoint.
    """
    ship_id_does_not_exist = 9999  # response_json['id']
    response: Response = client.put(f"/ships/{ship_id_does_not_exist}", json={
        "name": "Updated Ship",
        "classification": "Updated Classification",
        "sign": "Updated Sign",
        "speed": "Updated Speed",
        "captain": "Updated Captain",
        "comment": "Updated Comment",
        "url": "http://example.com/updated"
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.headers['content-type'] == 'application/json'
    response_json = response.json()
    assert response_json != None
    assert response_json['detail'] == f'Ship {ship_id_does_not_exist} not found'


def test_delete_non_existing_ship(client: TestClient) -> None:
    """
    Test the delete /ships/ endpoint for a non existing ship.
    """
    _create_mock_ships(client, 11)
    ship_id = 4711
    response: Response = client.delete(f"/ships/{ship_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_existing_ship(client: TestClient) -> None:
    """
    Test the delete /ships/ endpoint for existing ship.
    """
    _create_mock_ships(client, 11)
    ship_id = 5
    response = client.delete(f"/ships/{ship_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    r = client.get("/ships/")
    r_json = r.json()
    assert len(r_json) == 10


def test_upload_json_invalid_datatype(client: TestClient) -> None:
    """
    Test the /upload-json endpoint with invalid JSON data.s
    """
    payload = "invalid-json"
    response: Response = client.post("/ships/upload-json", content=payload,
                                     headers={"Content-Type": "application/json"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid JSON data" in response.json()["detail"]


def test_upload_json_invalid_json(client: TestClient) -> None:
    """
    Test the /upload-json endpoint with valid JSON data.
    """
    payload: dict[str, str] = {"key": "value"}
    response: Response = client.post("/ships/upload-json", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Invalid JSON data"}


def test_upload_single_ship_from_json(client: TestClient) -> None:
    """
    Test the /upload-json for single ship
    """
    with open('upload_single_ship.json', 'r') as file:
        payload = json.load(file)
    assert payload != None
    response: Response = client.post("/ships/upload-json", json=payload)
    # assert response.status_code == status.HTTP_201_CREATED
    # getter = client.get(f"/ships/1")
    # assert getter.status_code == status.HTTP_200_OK


def _test_upload_two_ships_from_json_upload(client: TestClient) -> None:
    """
    Test the /upload-json for single ship
    """
    with open('upload_single_ship.json', 'r') as file:
        payload = json.load(file)
    payload = [{
        "name": "Updated Ship1",
        "classification": "Updated Classification",
        "sign": "Updated Sign",
        "speed": "Updated Speed",
        "captain": "Updated Captain",
        "comment": "Updated Comment",
        "url": "http://example.com/updated"
    }, {
        "name": "Updated Ship2",
        "classification": "Updated Classification",
        "sign": "Updated Sign",
        "speed": "Updated Speed",
        "captain": "Updated Captain",
        "comment": "Updated Comment",
        "url": "http://example.com/updated"
    }]
    assert payload != None
    response: Response = client.post("/ships/upload-json", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    getter = client.get(f"/ships")
    assert getter.status_code == status.HTTP_200_OK
    assert len(getter.json()) == 2
