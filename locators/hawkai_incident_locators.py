from selenium.webdriver.common.by import By

# Incident row based on incident number - looking for the div containing INC number
def incident_row(incident_number):
    return (
        By.XPATH,
        f"//div[contains(text(), '{incident_number}')]/ancestor::tr"
    )

# Enrich with AI button inside that row
def enrich_ai_button(incident_number):
    return (
        By.XPATH,
        f"//div[contains(text(), '{incident_number}')]/ancestor::tr//button[contains(text(), 'Enrich with AI')]"
    )

# View button inside that row
def view_button(incident_number):
    return (
        By.XPATH,
        f"//div[contains(text(), '{incident_number}')]/ancestor::tr//button[contains(text(), 'View')]"
    )

# Alternative: If the incident number is in a specific cell
def incident_cell(incident_number):
    return (
        By.XPATH,
        f"//td[contains(@class, 'px-3')]//div[contains(text(), '{incident_number}')]"
    )

# AI Recommendation section in popup/modal
AI_RECOMMENDATION_SECTION = (
    By.XPATH,
    "//*[contains(text(), 'Recommendation') or contains(text(), 'AI Recommendations')]"
)

# Table rows locator
INCIDENT_ROWS = (By.XPATH, "//tbody/tr[@class='hover:bg-gray-50']")

# Action buttons container
def action_buttons_container(incident_number):
    return (
        By.XPATH,
        f"//div[contains(text(), '{incident_number}')]/ancestor::tr//div[@class='flex flex-col gap-1']"
    )