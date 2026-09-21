from behave import when, then
from pages.rag_agent_page import RagAgentPage
from utilities.helper_functions import take_screenshot
import time


@when("user switches to RAG Agents tab")
def step_switch_to_rag_agents(context):
    """Switch from Knowledge Base to RAG Agents tab"""
    print("🔄 Step: Switching to RAG Agents tab")
    
    # Initialize RAG Agent page
    context.rag_page = RagAgentPage(context.driver)
    
    # Switch to RAG Agents tab
    context.rag_page.switch_to_rag_agents_tab()


@when("User clicks on Create RAG Agent")
def step_click_create_rag(context):
    """Click on Create RAG Agent button"""
    print("🔄 Step: Clicking Create RAG Agent")
    context.rag_page.click_create_rag_agent()


@when("User enters Agent Name")
def step_enter_agent_name(context):
    """Enter agent name"""
    print("🔄 Step: Entering Agent Name")
    context.rag_page.enter_agent_name()


@when("User selects Provider as Anthropic")
def step_select_provider(context):
    """Select Anthropic as provider"""
    print("🔄 Step: Selecting Provider as Anthropic")
    context.rag_page.select_provider_anthropic()


@when("User selects Model from dropdown")
def step_select_model(context):
    """Select model from dropdown"""
    print("🔄 Step: Selecting Model")
    context.rag_page.select_model()


@when("User selects Category Infrastructure Provisioning")
def step_select_category(context):
    """Select Infrastructure Provisioning category"""
    print("🔄 Step: Selecting Category")
    context.rag_page.select_infrastructure_category()


@when("User clicks on Create RAG Agent button")
def step_submit_rag(context):
    """Click submit button to create RAG Agent"""
    print("🔄 Step: Clicking Create RAG Agent button")
    context.rag_page.click_submit_create_rag()


@then("RAG Agent should be created and visible on UI")
def step_verify_rag_created(context):
    """Verify RAG Agent was created"""
    print("🔄 Step: Verifying RAG Agent creation")
    context.rag_page.verify_rag_agent_created()
    take_screenshot(context.driver, "RAG_Agent_Created")


@when("User clicks on Edit button")
def step_click_edit(context):
    """Click Edit button on created agent"""
    print("🔄 Step: Clicking Edit button")
    context.rag_page.click_edit_button()


@when("User updates Agent Name")
def step_update_agent_name(context):
    """Update agent name in edit modal"""
    print("🔄 Step: Updating Agent Name")
    context.rag_page.update_agent_name()


@when("User changes Provider to Amazon")
def step_change_provider(context):
    """Change provider to Amazon"""
    print("🔄 Step: Changing Provider to Amazon")
    context.rag_page.change_provider_to_amazon()


@when("User changes Model to Nova Premier Advanced 8k")
def step_change_model(context):
    """Change model to Nova"""
    print("🔄 Step: Changing Model to Nova")
    context.rag_page.change_model_to_nova()


@when("User clicks on Update RAG Agent button")
def step_click_update(context):
    """Click Update button"""
    print("🔄 Step: Clicking Update RAG Agent button")
    context.rag_page.click_update_rag_agent()


@then("Updated RAG Agent should be visible on UI")
def step_verify_updated(context):
    """Verify agent was updated"""
    print("🔄 Step: Verifying updated agent")
    context.rag_page.verify_updated_agent()
    take_screenshot(context.driver, "RAG_Agent_Updated")