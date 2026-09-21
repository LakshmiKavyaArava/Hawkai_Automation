Feature: Incident AI Recommendation Flow

  Scenario: Create incident and validate AI recommendations in HawkAI
    Given user creates incident via ServiceNow API
    When user logs into HawkAI application
    And user clicks Enrich with AI
    And user clicks on view for that incident
    Then AI recommendations should be displayed