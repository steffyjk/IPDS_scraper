from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()

driver = webdriver.Chrome()

# Open the target website
url = os.environ.get("GOV_URL")
driver.get(url)

try:
    # Wait for the page to load and find the required elements
    wait = WebDriverWait(driver, 2)
    # Screenshot the page
    driver.save_screenshot('screenshot.png')



finally:
    # Close the browser when done
    driver.quit()
