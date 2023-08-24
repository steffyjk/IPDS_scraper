import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from dotenv import load_dotenv
import os
load_dotenv()
email = os.environ.get("email")
pwd = os.environ.get("password")
google_collab_id = os.environ.get("google_collab_id")
driver = webdriver.Chrome()

driver.get(google_collab_id)

time.sleep(5)
icon = driver.find_element(By.CLASS_NAME, "left-pane-button:nth-child(4) paper-icon-button").click()
time.sleep(5)
print("===")
button_script = """
const button = document.querySelector('mwc-button[slot="primaryAction"]');
if (button) {
    button.click();
}
"""

driver.execute_script(button_script)

driver.find_element(By.ID, "identifierId").send_keys(email)
time.sleep(5)

# click on next
next_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//span[text()="Next"]'))
)

# Click the "Next" button
next_button.click()
time.sleep(5)
# Passwd
password_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, 'Passwd'))
)

# Input your password
password_input.send_keys(pwd)
time.sleep(3)
# click on next
next_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//span[text()="Next"]'))
)
next_button.click()
time.sleep(10)
driver.find_element(By.CLASS_NAME, "left-pane-button:nth-child(4) paper-icon-button").click()
time.sleep(5)
icon_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'iron-icon[icon="colab:file-upload"]'))
)

# Click the iron-icon element
icon_element.click()




