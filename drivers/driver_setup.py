# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# def get_driver():
#     options = Options()
#     options.add_argument("--start-maximized")
#     options.add_argument("--incognito")   # ✅ ADD THIS LINE

#     driver = webdriver.Chrome(options=options)
#     driver.implicitly_wait(10)
#     return driver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tempfile

def get_driver():
    options = Options()
    options.add_argument("--start-maximized")

    # use fresh temp profile every run
    options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver
