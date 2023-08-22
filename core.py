import time

from selenium.webdriver.support.ui import WebDriverWait
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv

from Image_to_number_ml import convert_captcha_to_digits

load_dotenv()

driver = webdriver.Chrome()

# Open the target website
url = os.environ.get("GOV_URL")
driver.get(url)

try:
    # Wait for the page to load and find the required elements
    wait = WebDriverWait(driver, 2)
    driver.save_screenshot('screenshot.png')

    # Find the captcha
    img_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "img")))
    img_src = img_element.get_attribute("src")
    response = requests.get(img_src)
    with open("captcha_image.jpg", "wb") as f:
        f.write(response.content)
    wait = WebDriverWait(driver, 2)

    captcha = convert_captcha_to_digits()
    captcha_input_element = driver.find_element(By.NAME, 'CaptchaControl1')

    captcha_input_element.send_keys(captcha)
    time.sleep(5)

    submit_button = driver.find_element(By.NAME, 'btnGo')

    submit_button.click()
    time.sleep(5)
    # Find all <a> elements
    # Currently working now @22.08.2023
    try:
        a_elements = driver.find_elements(By.TAG_NAME, 'a')
        for i in a_elements:
            print(i.text)
    except Exception as e:
        print("===>e", e)




except Exception:
    print("there is some errorf")
