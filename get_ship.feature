# content of features/test_get_ships_limit.feature

Feature: Startrek API
    A site where you can manage data on vessels from the startrek uniiverse

    Scenario: I want to get a specific ship from the API by its ID
        Given The ship DB contains at more than 2 ships
        # And I have an article

        When I query for ship with ID 2

        Then I should get the ship with ID 2