# -- FILE: features/test_get_ships_limit.feature
Feature: Show how to use BDD to build an API

  Scenario: Retrieve a specific Ship from the DB
    Given DB contains at least 3 ships
     When we query for ship with ID 2
     Then the FastAPI backend will return the ship with ID 2