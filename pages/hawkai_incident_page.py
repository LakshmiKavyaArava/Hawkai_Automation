from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from locators.hawkai_incident_locators import *
from config.config import LOGIN_URL, USERNAME, PASSWORD
from pages.login_page import LoginPage
import time


class HawkAIIncidentPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)  # Reduced from 60 to 30
        self.short_wait = WebDriverWait(driver, 10)  # New short wait
        self.login_page = LoginPage(driver)

    def login(self):
        self.login_page.open(LOGIN_URL)
        self.login_page.login(USERNAME, PASSWORD)

        # Wait for table to load by checking for rows
        self.wait.until(
            EC.presence_of_element_located(INCIDENT_ROWS)
        )
        print("Successfully logged in and table loaded")

    def find_incident_row(self, incident_number):
        """Find and return the row containing the incident"""
        try:
            row = self.short_wait.until(  # Use short_wait here
                EC.presence_of_element_located(
                    incident_row(incident_number)
                )
            )
            return row
        except:
            print(f"Could not find incident row for {incident_number}")
            # Try to find by partial text if exact match fails
            alt_locator = (By.XPATH, f"//div[contains(text(), '{incident_number[-6:]}')]/ancestor::tr")
            return self.wait.until(EC.presence_of_element_located(alt_locator))

    def click_enrich_ai(self, incident_number):
        # First ensure incident_number is a string
        incident_number = str(incident_number)
        
        # Wait for the row to be visible
        self.find_incident_row(incident_number)
        
        # Find and click the Enrich with AI button
        enrich_btn = self.short_wait.until(  # Use short_wait
            EC.element_to_be_clickable(
                enrich_ai_button(incident_number)
            )
        )

        # Scroll into view and click
        self.driver.execute_script("arguments[0].scrollIntoView(true);", enrich_btn)
        time.sleep(0.5)  # Reduced from 1 to 0.5
        self.driver.execute_script("arguments[0].click();", enrich_btn)

        print(f"Clicked Enrich with AI for incident {incident_number}")

        # Reduced wait time for enrichment process
        time.sleep(8)  # Reduced from 20 to 8 seconds
        
        # Optional: Quick check for AI enriched indicator
        try:
            self.short_wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//div[contains(text(), '{incident_number}')]/ancestor::tr//*[contains(text(), 'AI')]")
                )
            )
        except:
            print("AI enrichment indicator not found, but continuing...")

    def click_view(self, incident_number):
        incident_number = str(incident_number)
        
        # Ensure the row is present
        self.find_incident_row(incident_number)
        
        # Find and click the View button
        view_btn = self.short_wait.until(  # Use short_wait
            EC.element_to_be_clickable(
                view_button(incident_number)
            )
        )

        self.driver.execute_script("arguments[0].scrollIntoView(true);", view_btn)
        time.sleep(0.5)  # Reduced from 1 to 0.5
        self.driver.execute_script("arguments[0].click();", view_btn)
        print(f"Clicked View for incident {incident_number}")
        
        # Add a small wait for the modal/popup to appear
        time.sleep(2)  # Wait for modal to load

    def validate_ai_recommendation(self):
        # Wait for AI recommendation section to appear (might be in a modal)
        try:
            self.short_wait.until(  # Use short_wait
                EC.visibility_of_element_located(
                    AI_RECOMMENDATION_SECTION
                )
            )
            print("AI Recommendations validated successfully")
            time.sleep(1)  # Brief pause to see the recommendation before screenshot
            return True
        except:
            # Try alternative locators
            alt_locators = [
                (By.XPATH, "//*[contains(text(), 'AI Suggestion')]"),
                (By.XPATH, "//*[contains(text(), 'Recommended Action')]"),
                (By.XPATH, "//div[contains(@class, 'recommendation')]")
            ]
            
            for locator in alt_locators:
                try:
                    self.short_wait.until(EC.visibility_of_element_located(locator))
                    print("AI Recommendations validated successfully (alternative locator)")
                    time.sleep(1)
                    return True
                except:
                    continue
            
            raise Exception("AI Recommendations not found")