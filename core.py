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
        region_name_elements = driver.find_elements(By.TAG_NAME, 'a')
        region_names = [{i.text: []} for i in region_name_elements]
        # print("This is the region names: ", region_names)
        driver.find_element(By.TAG_NAME, 'a').click()
        time.sleep(5)
        sub_region_ele = driver.find_elements(By.TAG_NAME, 'a')
        nex = []
        for i in sub_region_ele:
            nex.append(i.text)
        # print("===>", nex)
        driver.find_element(By.TAG_NAME, 'a').click()
        time.sleep(3)
        item_divs = driver.find_elements(By.CLASS_NAME, "dg_Item")
        # for div in item_divs:
        time.sleep(5)
        div = item_divs[0]

        td = div.find_elements(By.TAG_NAME, "td")
        time.sleep(3)
        # for i in td:
        # print(i.text)
        a_tag = div.find_elements(By.TAG_NAME, "a")
        time.sleep(3)
        apl_card = a_tag[1].click()
        time.sleep(5)

        card_lists = driver.find_elements(By.CLASS_NAME, "dg_Item")
        time.sleep(3)
        first_card = card_lists[0]
        internal = first_card.find_elements(By.TAG_NAME, "td")
        time.sleep(3)
        final_data = {
            "id": internal[0].text,
            "card_holder_name": internal[1].text,
            "hof_as_per_NFSA": internal[2].text,
            "ration_card_no": internal[3].text,
            "card_category": internal[4].text,
            "family_member": internal[5].text,
            "LPG_status": internal[6].text,
            "PNG_status": internal[7].text,
            "addr1": internal[8].text,
            "village": internal[9].text,
            "other_member": []
        }
        card_link = first_card.find_element(By.TAG_NAME, "a").click()
        time.sleep(3)
        members = driver.find_elements(By.CLASS_NAME, "dg_Item")
        time.sleep(3)
        for mem in members:
            mem_detail = mem.find_elements(By.TAG_NAME, "td")
            time.sleep(3)
            final_data["other_member"].append({
                "sr_no": mem_detail[0].text,
                "member_name": mem_detail[1].text,
                "age": mem_detail[2].text,
                "gender": mem_detail[3].text,
                "relation": mem_detail[4].text,
            })

        print(final_data)
        # Convert data to JSON string
        import json

        json_string = json.dumps(final_data, ensure_ascii=False, indent=4)

        # Specify the file name you want to save
        file_name = "output_data.json"

        # Write JSON string to a file
        with open(file_name, "w", encoding="utf-8") as json_file:
            json_file.write(json_string)

        print(f"Data has been saved to '{file_name}'.")




    except Exception as e:
        print("===>e", e)




except Exception as e:
    print("there is some error", e)
