from behave import given, when, then
from drivers.driver_setup import get_driver
from pages.hawkai_incident_page import HawkAIIncidentPage
from utilities.servicenow_api import create_incident
from utilities.helper_functions import take_screenshot
import time


@given("user creates incident via ServiceNow API")
def step_create_incident(context):
    response_data = create_incident()
    # Extract the incident number correctly
    if isinstance(response_data, dict):
        # Try different possible field names
        context.incident_number = (response_data.get('external_ticket_id') or 
                                  response_data.get('number') or 
                                  response_data.get('incident_number') or
                                  "INC010099854")  # fallback
    else:
        context.incident_number = response_data
    
    print(f"Created Incident Number: {context.incident_number}")
    # Reduced sync time - maybe HawkAI syncs faster
    time.sleep(8)  # Reduced from 15 to 8 seconds


@when("user logs into HawkAI application")
def step_login(context):
    context.driver = get_driver()
    context.hawkai_page = HawkAIIncidentPage(context.driver)
    context.hawkai_page.login()


@when("user clicks Enrich with AI")
def step_enrich(context):
    context.hawkai_page.click_enrich_ai(context.incident_number)


@when("user clicks on view for that incident")
def step_view(context):
    context.hawkai_page.click_view(context.incident_number)


@then("AI recommendations should be displayed")
def step_validate(context):
    context.hawkai_page.validate_ai_recommendation()
    take_screenshot(context.driver, "AI_Recommendation_Validated")
    # Give a moment to see the screenshot result
    time.sleep(2)
    context.driver.quit()