import allure
from allure_commons.types import AttachmentType

def after_step(context, step):
    if step.status == "failed":
        screenshot = context.driver.get_screenshot_as_png()
        allure.attach(
            screenshot,
            name="Failure Screenshot",
            attachment_type=AttachmentType.PNG
        )