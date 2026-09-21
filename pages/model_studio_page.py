from locators.model_studio_locators import *
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, os


class ModelStudioPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.kb_name = None

    # ================= NAVIGATION =================

    def open_model_studio(self):
        self.wait.until(EC.element_to_be_clickable(MODEL_STUDIO_MENU)).click()

    def open_knowledge_base_tab(self):
        self.wait.until(EC.element_to_be_clickable(KNOWLEDGE_BASE_TAB)).click()

    def click_new_knowledge_base(self):
        self.wait.until(EC.element_to_be_clickable(NEW_KB_BUTTON)).click()

    # ================= CREATE KB =================

    def fill_knowledge_base_form(self, name, description, category):
        self.wait.until(EC.visibility_of_element_located(KB_NAME_INPUT)).send_keys(name)
        self.driver.find_element(*KB_DESCRIPTION_INPUT).send_keys(description)
        Select(self.driver.find_element(*CATEGORY_DROPDOWN)).select_by_visible_text(category)
        self.kb_name = name

    def submit_kb(self):
        self.driver.find_element(*CREATE_BUTTON).click()
        time.sleep(5)

    def open_created_kb(self):
        kb = (By.XPATH, f"//*[contains(text(), '{self.kb_name}')]")
        self.wait.until(EC.element_to_be_clickable(kb)).click()
        time.sleep(2)

    # ================= UPLOAD =================

    def open_upload_popup(self):
        self.wait.until(EC.element_to_be_clickable(UPLOAD_DOCUMENT_BUTTON)).click()

    def upload_document(self, file_name):
        file_path = os.path.join(os.getcwd(), "testdata", file_name)
        print("Uploading:", file_path)

        file_input = self.wait.until(EC.presence_of_element_located(CHOOSE_FILE_INPUT))
        file_input.send_keys(file_path)

        time.sleep(2)
        self.driver.find_element(*UPLOAD_PROCESS_BUTTON).click()

    # ================= VALIDATE UPLOAD =================

    def validate_upload_success(self, doc_name="sample_sop"):
        wait = WebDriverWait(self.driver, 60)

        print("Waiting for processing...")

        success = wait.until(EC.visibility_of_element_located((
            By.XPATH, "//*[contains(text(),'Document processed successfully')]"
        )))

        close_btn = wait.until(EC.visibility_of_element_located((
            By.XPATH, "//button[normalize-space()='Close']"
        )))

        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", close_btn)
        print("Upload modal closed")

        try:
            wait.until(EC.invisibility_of_element(success))
        except:
            pass

        print("Re-opening KB")
        self.open_created_kb()
        time.sleep(3)

    # ================= EDIT / REPLACE =================

    def click_edit_document(self, doc_name="sample_sop"):
        print("Clicking edit icon for:", doc_name)
        
        time.sleep(2)
        
        try:
            edit_btn = self.wait.until(EC.element_to_be_clickable((
                By.XPATH,
                f"//*[contains(text(),'{doc_name}')]/ancestor::div[contains(@class,'flex')]//button[1]"
            )))
            
            self.driver.execute_script("arguments[0].scrollIntoView(true);", edit_btn)
            time.sleep(1)
            
            try:
                edit_btn.click()
            except:
                self.driver.execute_script("arguments[0].click();", edit_btn)
                
            print("✅ Edit button clicked")
            
        except Exception as e:
            print(f"❌ Error clicking edit button: {str(e)}")
            
            try:
                edit_btn = self.wait.until(EC.element_to_be_clickable((
                    By.XPATH,
                    f"(//*[contains(text(),'{doc_name}')]/following::button[.//*[name()='svg']])[1]"
                )))
                self.driver.execute_script("arguments[0].click();", edit_btn)
                print("✅ Edit button clicked via alternative selector")
            except:
                raise

    def replace_document(self, new_file):
        file_path = os.path.join(os.getcwd(), "testdata", new_file)

        if not os.path.exists(file_path):
            raise Exception(f"File not found: {file_path}")

        print(f"Replacing with: {file_path}")

        wait = WebDriverWait(self.driver, 30)

        try:
            wait.until(EC.visibility_of_element_located((
                By.XPATH,
                "//*[contains(text(),'Replace Document')]"
            )))
            print("✅ Replace modal opened")
        except:
            print("❌ Replace modal title not found")
            self.driver.save_screenshot("replace_modal_error.png")
            raise

        time.sleep(2)

        file_input = None
        
        try:
            file_input = wait.until(EC.presence_of_element_located((
                By.XPATH,
                "//div[contains(.,'Replace Document')]//input[@type='file']"
            )))
            print("✅ Found file input with original selector")
        except:
            print("⚠️ Original selector failed, trying alternatives...")
            
            try:
                file_input = wait.until(EC.presence_of_element_located((
                    By.XPATH,
                    "//div[contains(@class,'space-y-2')]//input[@type='file']"
                )))
                print("✅ Found file input with space-y-2 selector")
            except:
                try:
                    file_input = wait.until(EC.presence_of_element_located((
                        By.XPATH,
                        "//input[@type='file']"
                    )))
                    print("✅ Found file input with generic selector")
                except:
                    try:
                        file_input = wait.until(EC.presence_of_element_located((
                            By.XPATH,
                            "//div[contains(text(),'Choose File')]/preceding::input[@type='file'] | //input[@accept='.pdf, .docx, .txt, .md']"
                        )))
                        print("✅ Found file input with accept attribute selector")
                    except:
                        raise

        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", file_input)
            time.sleep(1)
            
            self.driver.execute_script("""
                arguments[0].style.display='block'; 
                arguments[0].style.visibility='visible'; 
                arguments[0].style.opacity='1';
                arguments[0].style.height='auto';
                arguments[0].style.width='auto';
                arguments[0].style.position='relative';
                arguments[0].style.zIndex='9999';
            """, file_input)
            
            file_input.send_keys(file_path)
            print("✅ File injected directly to input - system dialog avoided")
            
        except Exception as e:
            print(f"❌ Error interacting with file input: {str(e)}")
            try:
                self.driver.execute_script(
                    "arguments[0].value = arguments[1];",
                    file_input, file_path
                )
                print("✅ File injected via JavaScript - system dialog avoided")
            except:
                print("❌ JavaScript injection also failed")
                raise

        try:
            upload_btn = wait.until(EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(.,'Upload & Process')]"
            )))
            
            self.driver.execute_script("arguments[0].scrollIntoView(true);", upload_btn)
            time.sleep(1)
            
            try:
                upload_btn.click()
                print("✅ Clicked upload button")
            except:
                self.driver.execute_script("arguments[0].click();", upload_btn)
                print("✅ Clicked upload button via JavaScript")
                
            print("✅ Replace upload triggered")
            
        except Exception as e:
            print(f"❌ Error clicking upload button: {str(e)}")
            
            try:
                upload_btn = wait.until(EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[contains(.,'Upload')]"
                )))
                self.driver.execute_script("arguments[0].click();", upload_btn)
                print("✅ Clicked generic upload button")
            except:
                raise
        
        time.sleep(2)

    def validate_replace_success(self):
        wait = WebDriverWait(self.driver, 60)

        try:
            print("Waiting for processing to complete...")
            success = wait.until(EC.visibility_of_element_located((
                By.XPATH, "//*[contains(text(),'processed successfully')]"
            )))
            
            print("✅ Processing completed successfully")
            time.sleep(2)
            
            print("Replace success - modal ready for screenshot")
            return success
            
        except Exception as e:
            print(f"❌ Replace popup not detected: {str(e)}")
            self.driver.save_screenshot("replace_validation_error.png")
            raise

    def close_success_modal(self):
        try:
            close_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Close']"))
            )
            self.driver.execute_script("arguments[0].click();", close_btn)
            print("✅ Closed success modal after screenshot")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Close button not found: {str(e)}")

    # ================= DELETE DOCUMENT =================

    def delete_document(self, doc_name="sample_sop_edit"):
        wait = WebDriverWait(self.driver, 20)

        print("🔁 Re-opening KB for delete context...")
        self.open_created_kb()
        time.sleep(3)

        print(f"🗑 Deleting document: {doc_name}")

        # Find and click delete button
        delete_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            f"//*[contains(text(),'{doc_name}')]/ancestor::div[contains(@class,'border')]//button[.//*[contains(@class,'lucide-trash2')]]"
        )))

        # Scroll to delete button
        self.driver.execute_script("arguments[0].scrollIntoView(true);", delete_btn)
        time.sleep(1)

        # Click delete
        try:
            delete_btn.click()
            print("🗑 Delete button clicked")
        except:
            self.driver.execute_script("arguments[0].click();", delete_btn)
            print("🗑 Delete button clicked via JavaScript")

        # Wait a moment for alert to appear
        time.sleep(2)

        # Handle browser alert
        try:
            alert = wait.until(EC.alert_is_present())
            alert_text = alert.text
            print(f"📋 Alert text: {alert_text}")
            alert.accept()
            print("✅ Delete confirmed via browser alert")
        except TimeoutException:
            print("❌ No alert appeared after clicking delete")
            self.driver.save_screenshot("no_alert_found.png")
            raise

        # Wait for deletion to process
        time.sleep(3)
        print("✅ Document deleted successfully")
        
        try:
            print("❌ Closing document view...")
            close_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'lucide-x')]"))
            )
            self.driver.execute_script("arguments[0].click();", close_btn)
            time.sleep(2)
            print("✅ Document view closed")
        except Exception as e:
            print("⚠ Close button not found:", str(e))

    # ================= UPLOAD AFTER DELETE =================

    def upload_document_after_delete(self, file_name):
        """
        Upload a document after deletion - handles the case where no documents exist
        and we need to click the main Upload Document button again
        """
        print(f"📤 Uploading document after delete: {file_name}")
        
        # Wait a moment for the page to be ready
        time.sleep(2)
        
        try:
            # Check if we're still in the KB detail view
            # Look for any indicator that we're in the KB view
            upload_btn_present = len(self.driver.find_elements(*UPLOAD_DOCUMENT_BUTTON)) > 0
            
            if not upload_btn_present:
                # If upload button not found, we might have been redirected
                # Try to reopen the KB
                print("⚠ Upload button not found, reopening KB...")
                self.open_created_kb()
                time.sleep(2)
            
            # Click the Upload Document button (main one, not in modal)
            upload_btn = self.wait.until(EC.element_to_be_clickable(UPLOAD_DOCUMENT_BUTTON))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", upload_btn)
            time.sleep(1)
            upload_btn.click()
            print("✅ Upload button clicked")
            
            # Now upload the document using existing method
            file_path = os.path.join(os.getcwd(), "testdata", file_name)
            print("Uploading:", file_path)
            
            # Wait for file input to be present
            file_input = self.wait.until(EC.presence_of_element_located(CHOOSE_FILE_INPUT))
            file_input.send_keys(file_path)
            
            time.sleep(2)
            
            # Click Upload & Process button
            upload_process_btn = self.wait.until(EC.element_to_be_clickable(UPLOAD_PROCESS_BUTTON))
            upload_process_btn.click()
            print("✅ Upload & Process clicked")
            
            # Wait for success message and CLOSE IT before returning
            self.validate_and_close_upload_success(file_name.split('.')[0])
            
            print("✅ Document uploaded successfully after delete and modal closed")
            
        except Exception as e:
            print(f"❌ Error uploading document after delete: {str(e)}")
            self.driver.save_screenshot("upload_after_delete_error.png")
            raise


    def validate_and_close_upload_success(self, doc_name="sample_sop"):
        """
        Wait for upload success message and close the modal
        This is a modified version that doesn't re-open the KB
        """
        wait = WebDriverWait(self.driver, 60)

        print("Waiting for processing...")
        
        # Wait for success message
        success = wait.until(EC.visibility_of_element_located((
            By.XPATH, "//*[contains(text(),'Document processed successfully')]"
        )))
        print("✅ Upload success message displayed")

        # Wait for and click Close button
        close_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[normalize-space()='Close']"
        )))
        
        time.sleep(1)
        
        # Click using JavaScript to avoid any interception issues
        self.driver.execute_script("arguments[0].click();", close_btn)
        print("✅ Upload success modal closed")

        # Wait for modal to disappear
        try:
            wait.until(EC.invisibility_of_element(success))
            print("✅ Modal confirmed closed")
        except:
            pass

        # Give a moment for the UI to settle
        time.sleep(2)

    # ================= KB LIST NAVIGATION =================

    def wait_for_kb_list(self):
        """Wait for KB list page to be fully loaded"""
        print("⏳ Waiting for KB list page...")
        
        try:
            # Wait for New Knowledge Base button to be visible (indicator of KB list)
            self.wait.until(EC.visibility_of_element_located(NEW_KB_BUTTON))
            time.sleep(2)
            print("✅ KB list page ready")
        except Exception as e:
            print(f"❌ Error waiting for KB list: {str(e)}")
            self.driver.save_screenshot("kb_list_wait_error.png")
            raise

    def go_to_kb_list(self):
        """Navigate back to Knowledge Base list page"""
        print("🔙 Navigating back to Knowledge Base list")
        
        try:
            # First, make sure no modals are open
            # Check for any modal overlay and try to close it
            try:
                # Look for any close buttons in modals
                modal_close_btns = self.driver.find_elements(By.XPATH, 
                    "//button[contains(@class, 'lucide-x')] | //button[normalize-space()='Close'] | //button[contains(@aria-label, 'Close')]")
                
                for btn in modal_close_btns:
                    if btn.is_displayed():
                        self.driver.execute_script("arguments[0].click();", btn)
                        print("✅ Closed a modal overlay")
                        time.sleep(1)
            except:
                pass
            
            # Wait a moment for any animations to complete
            time.sleep(2)
            
            # Click Knowledge Base tab again
            kb_tab = self.wait.until(EC.element_to_be_clickable(KNOWLEDGE_BASE_TAB))
            
            # Scroll into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", kb_tab)
            time.sleep(1)
            
            # Try normal click first
            try:
                kb_tab.click()
                print("✅ Knowledge Base tab clicked")
            except:
                # If intercepted, use JavaScript
                self.driver.execute_script("arguments[0].click();", kb_tab)
                print("✅ Knowledge Base tab clicked via JavaScript")
            
            # Wait until KB list is visible (New KB button appears)
            self.wait.until(EC.visibility_of_element_located(NEW_KB_BUTTON))
            
            time.sleep(2)
            print("✅ Successfully navigated to Knowledge Base list page")
            
        except Exception as e:
            print(f"❌ Error navigating to KB list: {str(e)}")
            self.driver.save_screenshot("navigate_to_kb_list_error.png")
            
            # Last resort: try refreshing the page
            try:
                print("⚠ Attempting page refresh as last resort...")
                self.driver.refresh()
                time.sleep(5)
                self.wait.until(EC.visibility_of_element_located(NEW_KB_BUTTON))
                print("✅ Navigation successful after refresh")
            except:
                raise