from selenium.webdriver.common.by import By

# ================= NAVIGATION =================
MODEL_STUDIO_MENU = (By.XPATH, "//span[text()='Model Studio']")
KNOWLEDGE_BASE_TAB = (By.XPATH, "//button[text()='Knowledge Bases']")

# ================= KB CREATION =================
NEW_KB_BUTTON = (By.XPATH, "//button[normalize-space()='New Knowledge Base']")
CREATE_BUTTON = (By.XPATH, "//button[contains(.,'Create Knowledge Base')]")

KB_NAME_INPUT = (By.XPATH, "//input[@placeholder]")
KB_DESCRIPTION_INPUT = (By.XPATH, "//textarea")
CATEGORY_DROPDOWN = (By.XPATH, "//label[contains(.,'Category')]/following::select[1]")

# ================= UPLOAD =================
UPLOAD_DOCUMENT_BUTTON = (By.XPATH, "//button[contains(., 'Upload Document')]")

# Scoped upload file input
CHOOSE_FILE_INPUT = (
    By.XPATH,
    "//div[contains(.,'Upload Document')]//input[@type='file']"
)

UPLOAD_PROCESS_BUTTON = (By.XPATH, "//button[contains(., 'Upload & Process')]")

# ================= REPLACE =================

# Pencil icon (edit)
EDIT_DOCUMENT_BUTTON = (
    By.XPATH,
    "(//button[.//*[name()='svg']])[last()-1]"
)

# Replace modal file input (VERY IMPORTANT)
REPLACE_FILE_INPUT = (
    By.XPATH,
    "//div[contains(.,'Replace Document')]//input[@type='file']"
)

REPLACE_UPLOAD_BUTTON = (
    By.XPATH,
    "//button[contains(.,'Upload & Process')]"
)
DOCUMENT_ROW = (By.XPATH, "//div[contains(@class,'border') and contains(@class,'rounded-lg')]")


# ================= DELETE =================

# More specific delete icon selector based on the UI
DELETE_DOCUMENT_BUTTON = (
    By.XPATH,
    "//button[.//*[contains(@class,'lucide-trash2')]]"
)
# Alternative: Find by the document row and then the delete button
DELETE_BUTTON_BY_DOCUMENT = (
    By.XPATH,
    "//*[contains(text(),'sample_sop_edit')]/ancestor::div[contains(@class,'border')]//button[.//*[contains(@class,'lucide-trash2')]]"
)

# For the browser confirmation alert - handled via switch_to.alert
# ================= CLOSE DOCUMENT PAGE =================

# Add this at the end of your locators file
CLOSE_DOCUMENT_BUTTON = (By.XPATH, "//button[contains(@class, 'lucide-x')]")