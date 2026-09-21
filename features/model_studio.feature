Feature: Model Studio Knowledge Base Lifecycle

  Scenario: Create KB, Upload, Replace and Delete Document
    Given user is logged in and on the dashboard
    When user navigates to Model Studio
    And user opens Knowledge Base section
    And user clicks on New Knowledge Base
    And user enters knowledge base details
    And user opens the created knowledge base
    And user uploads a document into knowledge base
    And user replaces the uploaded document
    And user deletes the document
    And user uploads document again and goes back to KB list
    Then knowledge base lifecycle should complete successfully