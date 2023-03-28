from python_rucaptcha import ImageCaptcha
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from python_rucaptcha import ReCaptchaV2
from PIL import Image
import time
import random as rd
import data
import os
import EmailRu

RUCAPTCHA_KEY = "66efca878697536a5466d24eb5c17aa1"

def solve_text(driver):
    while True:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img.styles-mobile__captchaImage--sHzh3")))

        element = driver.find_element(By.CSS_SELECTOR, "img.styles-mobile__captchaImage--sHzh3")
        driver.save_screenshot('screenshot.png')

        left = element.location['x'] + 450
        top = element.location['y']
        right = element.location['x'] + 1000
        bottom = element.location['y'] + 350

        im = Image.open('screenshot.png')
        im = im.crop((left, top, right, bottom))
        im.save('screenshot2.png')

        user_answer = ImageCaptcha.ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(captcha_file='screenshot2.png')

        os.remove('screenshot.png')
        os.remove('screenshot2.png')

        if not user_answer['error']:
            return user_answer['captchaSolve']

        EmailRu.findElem(driver, by='text', name="Не вижу код", sleep=True)


def solve_v2(driver):
    # G-ReCaptcha ключ сайта
    SITE_KEY = ""
    PAGE_URL = driver.current_url
    user_answer = ReCaptchaV2.ReCaptchaV2(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(site_key=SITE_KEY,
                                                                                       page_url=PAGE_URL)
    if not user_answer['error']:
       return user_answer['captchaSolve']
       print(user_answer['taskId'])
    elif user_answer['error']:
        # Тело ошибки, если есть
        print(user_answer['errorBody'])
        print(user_answer['errorBody'])

