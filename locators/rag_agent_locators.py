from selenium.webdriver.common.by import By

class RagAgentLocators:
    
    # Tabs
    RAG_AGENTS_TAB = (By.XPATH, "//button[text()='RAG Agents']")
    
    # Buttons
    CREATE_RAG_AGENT_BUTTON = (By.XPATH, "//button[contains(.,'Create RAG Agent')]")
    SUBMIT_CREATE_RAG = (By.XPATH, "//button[contains(.,'Create RAG Agent') and @type='button']")

    # Agent Details
    AGENT_NAME_INPUT = (By.XPATH, "//input[@placeholder='e.g. AWS Backup Incident Analyzer']")

    # Provider Dropdown (REAL SELECT ELEMENT)
    PROVIDER_DROPDOWN = (By.XPATH, "//div[@data-field='provider']//select")

    # Model dropdown (REAL <select> inside data-field="model_name")
    MODEL_DROPDOWN = (By.XPATH, "//div[@data-field='model_name']//select")

    # Categories - Infrastructure Provisioning (Radix checkbox UI)
    INFRA_CATEGORY = (By.XPATH, "//span[contains(text(),'Monitoring')]")

    SUBMIT_CREATE_RAG = (
        By.XPATH,
        "//div[@role='dialog']//button[.//text()[contains(.,'Create RAG Agent')] or contains(.,'Create RAG Agent')]"
    )

    # Created Agent Validation (card name)
    CREATED_AGENT_CARD = (By.XPATH, "//div[contains(@class,'card') and contains(.,'Monitoring_RAG_Agent_Test')]")

    EDIT_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Edit']"
    )
    
    EDIT_AGENT_NAME_INPUT = (
        By.XPATH,
        "//input[@placeholder='e.g. AWS Backup Incident Analyzer']"
    )

    # Provider dropdown (Edit modal)
    EDIT_PROVIDER_DROPDOWN = (
        By.XPATH,
        "//div[@data-field='provider']//select"
    )

    EDIT_MODEL_DROPDOWN = (
        By.XPATH,
        "//div[@data-field='model_name']//select"
    )

    UPDATE_RAG_BUTTON = (
        By.XPATH,
        "//div[@role='dialog']//button[@type='submit']"
    )
    
    # Updated agent visible in list
    UPDATED_AGENT_CARD = (
        By.XPATH,
        "//div[contains(text(),'Monitoring_RAG_Agent_Updated')]"
    )
    
    # Loading indicator
    LOADING_SPINNER = (By.XPATH, "//div[contains(@class, 'loading') or contains(@class, 'spinner')]")