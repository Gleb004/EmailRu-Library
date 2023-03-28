import EmailRu
from selenium import webdriver
import data
import json
import time
import random

while True:
    driver = webdriver.Chrome()
    try:
        ans = EmailRu.register_sel(driver, data.url_reg)
        pas = EmailRu.make_imap_sel(driver, ans.split(":")[1])
        result = f"{ans}:{pas}\n"

        out = open("emails_with_api.txt", "a")
        out.write(result)
        print(f"{ans}:{pas}")
        out.close()

    except Exception as e:
        print(e)
        driver.quit()

