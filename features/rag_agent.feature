Feature: RAG Agent Management in Model Studio

  Scenario: Create and Update RAG Agent
    Given user is logged in and on the dashboard
    When user navigates to Model Studio
    And user opens Knowledge Base section
    And user switches to RAG Agents tab
    And User clicks on Create RAG Agent
    And User enters Agent Name
    And User selects Provider as Anthropic
    And User selects Model from dropdown
    And User selects Category Infrastructure Provisioning
    And User clicks on Create RAG Agent button
    Then RAG Agent should be created and visible on UI
    
    When User clicks on Edit button
    And User updates Agent Name
    And User changes Provider to Amazon
    And User changes Model to Nova Premier Advanced 8k
    And User clicks on Update RAG Agent button
    Then Updated RAG Agent should be visible on UI