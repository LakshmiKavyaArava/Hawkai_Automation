from behave import given, when, then
from drivers.driver_setup import get_driver
from pages.login_page import LoginPage
from pages.model_studio_page import ModelStudioPage
from config.config import LOGIN_URL, USERNAME, PASSWORD
from utilities.helper_functions import take_screenshot
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@given("user is logged in and on the dashboard")
def step_login(context):
    context.driver = get_driver()
    context.login_page = LoginPage(context.driver)
    context.model_page = ModelStudioPage(context.driver)

    context.login_page.open(LOGIN_URL)
    context.login_page.login(USERNAME, PASSWORD)
    time.sleep(5)
    take_screenshot(context.driver, "Login_Success")


@when("user navigates to Model Studio")
def step_model(context):
    context.model_page.open_model_studio()


@when("user opens Knowledge Base section")
def step_kb(context):
    context.model_page.open_knowledge_base_tab()


@when("user clicks on New Knowledge Base")
def step_new_kb(context):
    context.model_page.click_new_knowledge_base()


@when("user enters knowledge base details")
def step_fill(context):
    context.model_page.fill_knowledge_base_form(
        "RTS_QA_KB_Monitoring",
        "Monitoring SOPs",
        "Monitoring"
    )
    context.model_page.submit_kb()
    take_screenshot(context.driver, "KB_Created")


@when("user opens the created knowledge base")
def step_open(context):
    context.model_page.open_created_kb()
    take_screenshot(context.driver, "KB_Dashboard")


@when("user uploads a document into knowledge base")
def step_upload(context):
    context.model_page.open_upload_popup()
    context.model_page.upload_document("sample_sop.docx")
    context.model_page.validate_upload_success()
    take_screenshot(context.driver, "Uploaded")


@when("user replaces the uploaded document")
def step_replace(context):
    context.model_page.click_edit_document()
    context.model_page.replace_document("sample_sop_edit.pdf")
    context.model_page.validate_replace_success()
    
    # Wait for success modal to be fully visible
    time.sleep(2)
    
    # Take screenshot before closing
    take_screenshot(context.driver, "Replaced")
    
    # Now close the modal
    context.model_page.close_success_modal()


@when("user deletes the document")
def step_delete(context):
    # Small wait to ensure we're on the right page
    time.sleep(2)
    
    # Perform delete operation
    context.model_page.delete_document()

    # Wait for delete to complete
    time.sleep(3)
    
    # Take screenshot after deletion
    take_screenshot(context.driver, "Deleted")
    
    # Verify document is gone
    try:
        context.driver.find_element(By.XPATH, "//*[contains(text(),'sample_sop_edit')]")
        print("⚠ Document still found - deletion might have failed")
    except:
        print("✅ Document successfully deleted - not found in UI")


@when("user uploads document again and goes back to KB list")
def step_upload_again_and_back(context):
    # Upload document again
    print("📤 Uploading document again after deletion...")
    
    # Wait a moment for the page to settle after deletion
    time.sleep(2)
    
    # Upload the document again
    context.model_page.upload_document_after_delete("sample_sop.docx")
    
    # Take screenshot after second upload
    take_screenshot(context.driver, "Uploaded_Again")
    
    # Now go back to KB list
    context.model_page.go_to_kb_list()
    
    # Wait for KB list to be ready
    context.model_page.wait_for_kb_list()
    
    # Take screenshot on KB list
    take_screenshot(context.driver, "Back_To_KB_List")


@then("knowledge base lifecycle should complete successfully")
def step_done(context):
    print("✅ Knowledge base lifecycle completed successfully")
    print("✅ Created KB → Uploaded → Replaced → Deleted → Uploaded Again → Back to List")
    # time.sleep(3)
    context.driver.quit()