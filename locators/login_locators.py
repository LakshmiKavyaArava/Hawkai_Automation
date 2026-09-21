# from selenium.webdriver.common.by import By

# # Login page locators
# USERNAME_INPUT = (By.ID, "email")
# PASSWORD_INPUT = (By.ID, "password")
# SIGNIN_BUTTON = (By.XPATH, "//button[contains(., 'Log in')]")

from selenium.webdriver.common.by import By

USERNAME_INPUT = (By.ID, "email")
PASSWORD_INPUT = (By.ID, "password")
SIGNIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")