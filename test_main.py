from typing import Any, Generator
from main import app
from routers.ships_router import get_session
import pytest
from fastapi.testclient import TestClient
from fastapi import status
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from settings import Settings
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
    response = client.get("/ships/6")
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
    response = client.put(f"/ships/{ship_id}", json={
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
    ship_id = 9999  # response_json['id']
    response = client.put(f"/ships/{ship_id}", json={
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
    assert response_json['detail'] == f'Ship {ship_id} not found'


def test_delete_non_existing_ship(client: TestClient) -> None:
    """
    Test the delete /ships/ endpoint for a non existing ship.
    """
    _create_mock_ships(client, 11)
    ship_id = 4711
    response = client.delete(f"/ships/{ship_id}")
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


def test_check_metrics_endpoint(client: TestClient) -> None:
    """
    Test the /metrics endpoint.
    """
    response = client.get("/metrics")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-type'].startswith(
        'text/plain; version=0.0.4')
    assert response.text.startswith(
        "# HELP python_gc_objects_collected_total Objects collected during gc")
