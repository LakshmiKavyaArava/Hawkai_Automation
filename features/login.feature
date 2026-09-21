Feature: Login functionality

  Scenario: Successful login with valid credentials
    Given user is on the login page
    When the user logs in with valid credentials
    And click on the login button
    Then the user should be navigated to the home page
