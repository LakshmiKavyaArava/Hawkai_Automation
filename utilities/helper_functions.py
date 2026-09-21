import allure
from allure_commons.types import AttachmentType
from datetime import datetime
import os

def take_screenshot(driver, name="screenshot"):
    folder = "reports/screenshots"
    os.makedirs(folder, exist_ok=True)

    file_name = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = os.path.join(folder, file_name)

    driver.save_screenshot(path)

    # Attach to Allure
    allure.attach.file(
        path,
        name=name,
        attachment_type=AttachmentType.PNG
    )

    print(f"📸 Screenshot saved: {path}")