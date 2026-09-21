from locators.login_locators import USERNAME_INPUT, PASSWORD_INPUT, SIGNIN_BUTTON
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class LoginPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def open(self, url: str):
        """Open login page"""
        try:
            self.driver.get(url)
            print(f"Opened URL: {url}")
            time.sleep(2)  # Wait for page to load
        except Exception as e:
            print(f"Error opening URL: {e}")
            raise

    def enter_username(self, username: str):
        """Enter username with wait"""
        try:
            el = self.wait.until(EC.presence_of_element_located(USERNAME_INPUT))
            el.clear()
            el.send_keys(username)
            print("Username entered")
        except TimeoutException:
            print("Username field not found")
            raise

    def enter_password(self, password: str):
        """Enter password with wait"""
        try:
            el = self.wait.until(EC.presence_of_element_located(PASSWORD_INPUT))
            el.clear()
            el.send_keys(password)
            print("Password entered")
        except TimeoutException:
            print("Password field not found")
            raise

    def click_sign_in(self):
        """Click sign in button with wait"""
        try:
            btn = self.wait.until(EC.element_to_be_clickable(SIGNIN_BUTTON))
            btn.click()
            print("Clicked Sign In button")
            time.sleep(3)  # Wait for navigation
        except TimeoutException:
            print("Sign in button not clickable")
            raise

    def login(self, username: str, password: str):
        """Complete login flow"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_sign_in()

    def wait_for_login_success(self):
        """Wait for login to complete (Sign In button disappears)"""
        try:
            self.wait.until(EC.invisibility_of_element_located(SIGNIN_BUTTON))
            print("Login successful - Sign In button disappeared")
        except TimeoutException:
            print("Login may have failed - Sign In button still visible")
            raise

    def is_logged_in(self):
        """Check if user is logged in"""
        try:
            # Check if URL changed or dashboard element appears
            current_url = self.driver.current_url
            if "dashboard" in current_url or "incidents" in current_url or "home" in current_url:
                return True
            return False
        except:
            return False