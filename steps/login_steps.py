from behave import given, when, then
from drivers.driver_setup import get_driver
from pages.login_page import LoginPage
from config.config import LOGIN_URL, USERNAME, PASSWORD
from utilities.helper_functions import take_screenshot
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time


# Example locator for something visible only after login
HOME_PAGE_INDICATOR = (By.XPATH, "//span[contains(text(),'Agentic AI')]")


@given("user is on the login page")
def step_open_login(context):
    context.driver = get_driver()
    context.login_page = LoginPage(context.driver)
    context.login_page.open(LOGIN_URL)


@when("the user logs in with valid credentials")
def step_enter_credentials(context):
    context.login_page.enter_username(USERNAME)
    context.login_page.enter_password(PASSWORD)


@when("click on the login button")
def step_click_login(context):
    context.login_page.click_sign_in()
    time.sleep(5)


@then("the user should be navigated to the home page")
def step_validate_login(context):

    wait = WebDriverWait(context.driver, 15)

    try:
        # Wait for something that appears only after successful login
        wait.until(EC.visibility_of_element_located(HOME_PAGE_INDICATOR))

        print("✅ Login successful")

        take_screenshot(context.driver, "Login_Successful")

    except TimeoutException:

        print("❌ Login failed")

        take_screenshot(context.driver, "Login_Failed")

        context.driver.quit()

        raise AssertionError("Login validation failed - Home page not loaded")

    context.driver.quit()