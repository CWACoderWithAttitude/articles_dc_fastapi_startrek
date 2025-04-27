# test_get_ship.py
from pytest_bdd import scenarios, given, when, then
from typing import Any, Generator
from fastapi.testclient import TestClient
from pytest_bdd import given
from main import app
from pytest_bdd import given, when, then
from fastapi import status
from test_utils.mock_ships import _create_mock_ships
from test_utils.fixtures import session_fixture, client_fixture

# Load the feature file
scenarios('get_ship.feature')


@given("The ship DB contains at more than 2 ships")
def the_ship_db_contains_more_than_two_ships(client: TestClient):
    _create_mock_ships(client, 3)
    ships = client.get("/ships/")
    assert ships.status_code == 200
    assert ships.headers["content-type"] == "application/json"
    ships_json = ships.json()
    assert len(ships_json) > 2


@when("I query for ship with ID 2")
def i_query_for_ship_with_id_2(client):
    id_to_query = 2
    response = client.get(f"/ships/{id_to_query}")
    assert response.status_code == status.HTTP_200_OK


@then("I should get the ship with ID 2")
def I_should_get_the_ship_with_ID_2(client: TestClient):
    id_to_query = 2
    response = client.get(f"/ships/{id_to_query}")
    response_json = response.json()
    assert response_json['id'] == 2
