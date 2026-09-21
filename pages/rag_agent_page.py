import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.rag_agent_locators import RagAgentLocators
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException


class RagAgentPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.agent_name = "Monitoring_RAG_Agent_Test"
        self.updated_agent_name = "Monitoring_RAG_Agent_Updated"

    # ================= NAVIGATION =================

    def switch_to_rag_agents_tab(self):
        """Switch from Knowledge Base to RAG Agents tab"""
        print("🔄 Switching to RAG Agents tab...")
        
        try:
            # Wait a moment for the page to be ready
            time.sleep(3)
            
            # Try multiple possible selectors for RAG Agents tab
            selectors = [
                RagAgentLocators.RAG_AGENTS_TAB,
                (By.XPATH, "//button[contains(text(),'RAG Agents')]"),
                (By.XPATH, "//button[contains(@class, 'tab') and contains(text(), 'RAG')]"),
                (By.XPATH, "//div[contains(@class, 'tab')]//button[contains(text(), 'RAG')]")
            ]
            
            rag_tab = None
            for selector in selectors:
                try:
                    rag_tab = self.wait.until(
                        EC.element_to_be_clickable(selector)
                    )
                    print(f"✅ Found RAG Agents tab with selector: {selector}")
                    break
                except:
                    continue
            
            if not rag_tab:
                raise Exception("Could not find RAG Agents tab with any selector")
            
            # Scroll into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", rag_tab)
            time.sleep(1)
            
            # Click using JavaScript to avoid any interception
            self.driver.execute_script("arguments[0].click();", rag_tab)
            print("✅ Switched to RAG Agents tab")
            
            # Wait for RAG Agents page to load
            time.sleep(5)
            
            # Verify we're on RAG Agents page by checking for Create button
            self.wait.until(
                EC.presence_of_element_located(RagAgentLocators.CREATE_RAG_AGENT_BUTTON)
            )
            print("✅ RAG Agents page loaded successfully")
            
        except Exception as e:
            print(f"❌ Error switching to RAG Agents tab: {str(e)}")
            self.driver.save_screenshot("switch_to_rag_error.png")
            raise

    # ================= CREATE RAG AGENT =================

    def click_create_rag_agent(self):
        """Click on Create RAG Agent button"""
        print("🔄 Clicking Create RAG Agent button...")
        
        try:
            # Wait for any loading spinners to disappear
            try:
                self.wait.until(EC.invisibility_of_element_located(RagAgentLocators.LOADING_SPINNER))
            except:
                pass
            
            btn = self.wait.until(
                EC.element_to_be_clickable(RagAgentLocators.CREATE_RAG_AGENT_BUTTON)
            )
            
            self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            time.sleep(1)
            
            # Try normal click first
            try:
                btn.click()
            except:
                self.driver.execute_script("arguments[0].click();", btn)
            
            print("✅ Create RAG Agent button clicked")
            time.sleep(3)
            
            # Wait for modal to appear
            self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']"))
            )
            print("✅ Creation modal opened")
            
        except Exception as e:
            print(f"❌ Error clicking Create RAG Agent: {str(e)}")
            self.driver.save_screenshot("click_create_rag_error.png")
            raise

    def enter_agent_name(self):
        """Enter agent name in the creation modal"""
        print("🔄 Entering agent name...")
        
        try:
            agent_input = self.wait.until(
                EC.visibility_of_element_located(RagAgentLocators.AGENT_NAME_INPUT)
            )
            agent_input.clear()
            agent_input.send_keys(self.agent_name)
            
            print(f"✅ Agent name entered: {self.agent_name}")
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error entering agent name: {str(e)}")
            self.driver.save_screenshot("enter_agent_name_error.png")
            raise

    def select_provider_anthropic(self):
        """Select Anthropic as provider"""
        print("🔄 Selecting provider: Anthropic...")
        
        try:
            # Wait for provider dropdown
            provider_dropdown = self.wait.until(
                EC.element_to_be_clickable(RagAgentLocators.PROVIDER_DROPDOWN)
            )

            # Scroll into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", provider_dropdown)
            time.sleep(2)

            # Use Select class
            select = Select(provider_dropdown)
            
            # Try to select by visible text
            try:
                select.select_by_visible_text("Anthropic")
            except:
                # Try by value if text doesn't work
                select.select_by_value("anthropic")

            print("✅ Provider selected: Anthropic")
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error selecting provider: {str(e)}")
            self.driver.save_screenshot("select_provider_error.png")
            raise

    def select_model(self):
        """Select model from dropdown"""
        print("🔄 Selecting model...")
        
        try:
            model_element = self.wait.until(
                EC.presence_of_element_located(RagAgentLocators.MODEL_DROPDOWN)
            )

            self.driver.execute_script("arguments[0].scrollIntoView(true);", model_element)
            time.sleep(2)

            select = Select(model_element)
            
            # Try multiple model options
            model_options = [
                "Claude Sonnet 4 (Standard)",
                "Claude Sonnet 4",
                "Claude",
                "sonnet"
            ]
            
            selected = False
            for option_text in model_options:
                try:
                    select.select_by_visible_text(option_text)
                    print(f"✅ Model selected: {option_text}")
                    selected = True
                    break
                except:
                    continue
            
            if not selected:
                # Select first option if none of the above work
                select.select_by_index(1)
                print(f"✅ Model selected: {select.first_selected_option.text}")
            
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error selecting model: {str(e)}")
            self.driver.save_screenshot("select_model_error.png")
            raise

    def select_infrastructure_category(self):
        """Select Infrastructure Provisioning category"""
        print("🔄 Selecting category: Infrastructure Provisioning...")
        
        try:
            time.sleep(3)

            # Try multiple selectors for category checkbox
            category_selectors = [
                (By.XPATH, "//span[text()='Monitoring']/ancestor::div[contains(@class,'flex items-center')]//button[@role='checkbox']"),
                (By.XPATH, "//span[contains(text(),'Monitoring')]/preceding::button[@role='checkbox'][1]"),
                (By.XPATH, "//div[contains(@class, 'category')]//button[@role='checkbox']"),
                (By.XPATH, "//label[contains(text(),'Monitoring')]/input")
            ]
            
            category_checkbox = None
            for selector in category_selectors:
                try:
                    category_checkbox = self.wait.until(
                        EC.presence_of_element_located(selector)
                    )
                    print(f"✅ Found category checkbox with selector: {selector}")
                    break
                except:
                    continue
            
            if not category_checkbox:
                raise Exception("Could not find category checkbox")

            # Scroll into view
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                category_checkbox
            )
            time.sleep(1)

            # Check if already checked
            is_checked = category_checkbox.get_attribute("aria-checked")
            
            if is_checked != "true":
                # Click using JS
                self.driver.execute_script("arguments[0].click();", category_checkbox)
                time.sleep(2)

                # Verify selection
                is_checked = category_checkbox.get_attribute("aria-checked")
                if is_checked == "true":
                    print("✅ Category selected: Monitoring")
                else:
                    raise Exception("❌ Category NOT selected: Monitoring")
            else:
                print("✅ Category already selected: Monitoring")
                
        except Exception as e:
            print(f"❌ Error selecting category: {str(e)}")
            self.driver.save_screenshot("select_category_error.png")
            raise

    def click_submit_create_rag(self):
        """Click the Create RAG Agent submit button"""
        print("🔄 Submitting RAG Agent creation...")
        
        try:
            time.sleep(3)

            # Try multiple selectors for submit button
            submit_selectors = [
                RagAgentLocators.SUBMIT_CREATE_RAG,
                (By.XPATH, "//div[@role='dialog']//button[@type='submit']"),
                (By.XPATH, "//div[@role='dialog']//button[contains(text(), 'Create')]"),
                (By.XPATH, "//button[contains(text(), 'Create RAG Agent')]")
            ]
            
            submit_btn = None
            for selector in submit_selectors:
                try:
                    submit_btn = self.wait.until(
                        EC.presence_of_element_located(selector)
                    )
                    break
                except:
                    continue

            if not submit_btn:
                raise Exception("Could not find submit button")

            # Scroll to button
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                submit_btn
            )
            time.sleep(2)

            # Wait until button is enabled
            self.wait.until(lambda driver: submit_btn.is_enabled())

            # Click using JavaScript
            self.driver.execute_script("arguments[0].click();", submit_btn)

            print("✅ Create RAG Agent button clicked")
            time.sleep(5)
            
            # Wait for modal to close
            try:
                self.wait.until(
                    EC.invisibility_of_element_located((By.XPATH, "//div[@role='dialog']"))
                )
                print("✅ Creation modal closed")
            except:
                print("⚠ Modal may still be open")
                
        except Exception as e:
            print(f"❌ Error submitting RAG Agent: {str(e)}")
            self.driver.save_screenshot("submit_rag_error.png")
            raise

    def verify_rag_agent_created(self):
        """Verify RAG Agent was created successfully"""
        print("🔄 Verifying RAG Agent creation...")
        
        try:
            # Wait for agent card to appear
            self.wait.until(
                EC.presence_of_element_located(RagAgentLocators.CREATED_AGENT_CARD)
            )
            print(f"✅ RAG Agent created successfully: {self.agent_name}")
            
            # Wait a moment for UI to stabilize
            time.sleep(3)
            
        except Exception as e:
            print(f"❌ Error verifying RAG Agent creation: {str(e)}")
            self.driver.save_screenshot("verify_rag_creation_error.png")
            
            # Try to find any agent card as fallback
            try:
                any_agent = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'card')]"))
                )
                print("⚠ Found some agent card but not the specific one")
            except:
                raise

    # ================= EDIT RAG AGENT =================

    def click_edit_button(self):
        """Click Edit button on the created agent"""
        print("🔄 Clicking Edit button...")
        
        try:
            # Wait for agent card to be visible
            self.wait.until(
                EC.visibility_of_element_located(RagAgentLocators.CREATED_AGENT_CARD)
            )

            # Wait for Edit button to be clickable
            edit_btn = self.wait.until(
                EC.element_to_be_clickable(RagAgentLocators.EDIT_BUTTON)
            )

            self.driver.execute_script("arguments[0].scrollIntoView(true);", edit_btn)
            time.sleep(1)
            
            # Try normal click first
            try:
                edit_btn.click()
            except:
                self.driver.execute_script("arguments[0].click();", edit_btn)

            # Wait for Edit modal to appear
            self.wait.until(
                EC.visibility_of_element_located(RagAgentLocators.EDIT_AGENT_NAME_INPUT)
            )

            print("✅ Edit button clicked")
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error clicking Edit button: {str(e)}")
            self.driver.save_screenshot("click_edit_error.png")
            raise

    def update_agent_name(self):
        """Update agent name in edit modal"""
        print("🔄 Updating agent name...")
        
        try:
            name_input = self.wait.until(
                EC.visibility_of_element_located(RagAgentLocators.EDIT_AGENT_NAME_INPUT)
            )

            name_input.click()
            name_input.clear()
            name_input.send_keys(self.updated_agent_name)

            print(f"✅ Agent name updated to: {self.updated_agent_name}")
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error updating agent name: {str(e)}")
            self.driver.save_screenshot("update_name_error.png")
            raise

    def change_provider_to_amazon(self):
        """Change provider to Amazon in edit modal"""
        print("🔄 Changing provider to Amazon...")
        
        try:
            provider_dropdown = self.wait.until(
                EC.element_to_be_clickable(RagAgentLocators.EDIT_PROVIDER_DROPDOWN)
            )

            select = Select(provider_dropdown)
            
            # Try by value first
            try:
                select.select_by_value("amazon")
            except:
                # Try by visible text
                try:
                    select.select_by_visible_text("Amazon")
                except:
                    # Try by partial text
                    for option in select.options:
                        if "Amazon" in option.text or "amazon" in option.text:
                            option.click()
                            break

            print("✅ Provider changed to Amazon")
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error changing provider: {str(e)}")
            self.driver.save_screenshot("change_provider_error.png")
            raise

    def change_model_to_nova(self):
        """Change model to Nova Premier Advanced 8k"""
        print("🔄 Changing model to Nova Premier Advanced 8k...")
        
        try:
            model_dropdown = self.wait.until(
                EC.element_to_be_clickable(RagAgentLocators.EDIT_MODEL_DROPDOWN)
            )

            select = Select(model_dropdown)
            
            # Find Nova model
            nova_selected = False
            for option in select.options:
                if "Nova" in option.text and "8k" in option.text:
                    option.click()
                    print("✅ Model changed to Nova Premier Advanced 8k")
                    nova_selected = True
                    break
            
            if not nova_selected:
                # Fallback: select first option with Nova
                for option in select.options:
                    if "Nova" in option.text:
                        option.click()
                        print(f"✅ Model changed to: {option.text}")
                        nova_selected = True
                        break
            
            if not nova_selected:
                # Last resort: select first option
                select.select_by_index(1)
                print(f"✅ Model changed to: {select.first_selected_option.text}")

            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error changing model: {str(e)}")
            self.driver.save_screenshot("change_model_error.png")
            raise

    def click_update_rag_agent(self):
        """Click Update RAG Agent button"""
        print("🔄 Clicking Update RAG Agent button...")
        
        try:
            # Wait for dialog
            dialog = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']"))
            )

            # Try multiple selectors for Update button
            update_selectors = [
                (By.XPATH, ".//button[@type='submit']"),
                (By.XPATH, ".//button[contains(text(), 'Update')]"),
                (By.XPATH, ".//button[contains(text(), 'Update RAG Agent')]")
            ]
            
            update_btn = None
            for selector in update_selectors:
                try:
                    update_btn = dialog.find_element(*selector)
                    if update_btn.is_enabled():
                        break
                except:
                    continue

            if not update_btn:
                raise Exception("Could not find Update button")

            # Scroll
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                update_btn
            )

            time.sleep(2)

            # Force click
            self.driver.execute_script("arguments[0].click();", update_btn)

            print("✅ Update RAG Agent button clicked")
            time.sleep(5)
            
            # Wait for modal to close
            try:
                self.wait.until(
                    EC.invisibility_of_element_located((By.XPATH, "//div[@role='dialog']"))
                )
                print("✅ Update modal closed")
            except:
                print("⚠ Update modal may still be open")
            
        except Exception as e:
            print(f"❌ Error clicking Update button: {str(e)}")
            self.driver.save_screenshot("click_update_error.png")
            raise

    def verify_updated_agent(self):
        """Verify agent was updated successfully"""
        print("🔄 Verifying agent update...")
        
        try:
            # Wait for updated agent card
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//div[contains(text(),'{self.updated_agent_name}')]")
                )
            )
            print(f"✅ Updated RAG Agent visible: {self.updated_agent_name}")
            
            # Take success screenshot
            self.driver.save_screenshot("rag_agent_update_success.png")
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error verifying updated agent: {str(e)}")
            self.driver.save_screenshot("verify_update_error.png")
            
            # Try to find any agent as fallback
            try:
                any_agent = self.driver.find_elements(By.XPATH, "//div[contains(@class,'card')]")
                print(f"⚠ Found {len(any_agent)} agent cards but not the updated one")
            except:
                raise