from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from imaplib import IMAP4, IMAP4_SSL
import email
from datetime import timedelta, date
import twisted.mail.imap4
import json
import time
import random as rd
import data
import RuCaptcha

def gen(act):
    def name():
        return str(data.vec[rd.randint(0, len(data.vec) - 1)])

    def domain():
        return f"{name()}.{str(rd.randint(10, 99))}.{name()}.{str(rd.randint(100, 999))}".replace('\n', '')

    def password():
        line = ""
        for j in range(4):
            line += data.specL[rd.randint(0, len(data.specL) - 1)]
            line += data.smallL[rd.randint(0, len(data.smallL) - 1)]
            line += data.specL[rd.randint(0, len(data.specL) - 1)]
            line += data.bigL[rd.randint(0, len(data.bigL) - 1)]
        return str(line).replace('\n', '')

    if act == 'name': return name()
    elif act == 'password': return password()
    elif act == 'domain': return domain()
    elif act == 'R': return rd.randint(1, 25)
    elif act == 'month': return data.months[rd.randint(0, 11)]
    elif act == 'gender': return data.gender[rd.randint(0, 1)]
    elif act == 'year': return rd.randint(1980, 2010)

def findElem(driver, by, name, send=False, text='', wait=5.0, sleep=False):
    if by == 'text':
        try:
            WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.XPATH, f"//*[text() = '{name}']")))
            if text == '':
                driver.find_element(By.XPATH, f"//*[text() = '{name}']").click()
            else:
                driver.find_element(By.XPATH, f"//*[text() = '{name}']").clear()
                driver.find_element(By.XPATH, f"//*[text() = '{name}']").send_keys(text)
                if send: driver.find_element(By.XPATH, f"//*[text() = '{name}']").send_keys(Keys.ENTER)
        except: pass
    elif by == 'css':
        try:
            WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.CSS_SELECTOR, f"{name}")))
            if text == '':
                driver.find_element(By.CSS_SELECTOR, f"{name}").click()
            else:
                driver.find_element(By.CSS_SELECTOR, f"{name}").clear()
                driver.find_element(By.CSS_SELECTOR, f"{name}").send_keys(text)
                if send: driver.find_element(By.CSS_SELECTOR, f"{name}").send_keys(Keys.ENTER)
        except: pass
    elif by == 'name':
        try:
            WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.NAME, f"{name}")))
            if text == '':
                driver.find_element(By.NAME, f"{name}").click()
            else:
                driver.find_element(By.NAME, f"{name}").clear()
                driver.find_element(By.NAME, f"{name}").send_keys(text)
                if send: driver.find_element(By.NAME, f"{name}").send_keys(Keys.ENTER)
        except: pass
    elif by == 'placeholder':
        try:
            WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.XPATH, f"//input[@placeholder='{name}']")))
            if text == '':
                driver.find_element(By.XPATH, f"//input[@placeholder='{name}']").click()
            else:
                driver.find_element(By.XPATH, f"//input[@placeholder='{name}']").clear()
                driver.find_element(By.XPATH, f"//input[@placeholder='{name}']").send_keys(text)
                if send: driver.find_element(By.XPATH, f"//input[@placeholder='{name}']").send_keys(Keys.ENTER)
        except: pass
    elif by == 'id':
        try:
            WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.ID, name)))
            if text == '':
                driver.find_element(By.ID, name).click()
            else:
                driver.find_element(By.ID, name).clear()
                driver.find_element(By.ID, name).send_keys(text)
                if send: driver.find_element(By.ID, name).send_keys(Keys.ENTER)
        except: pass

    if sleep: time.sleep(wait / 10)

def welcome_page(driver, wait=5.0):
    commands = ['Настроить', 'Приступить к работе', 'Отменить']
    for action in commands:
        findElem(driver, by='text', name=action, wait=3)
        time.sleep(1)

def make_imap_sel(driver, ac_password, wait=5.0):
    findElem(driver, by='css', name="span.ph-dropdown-icon", wait=wait)
    findElem(driver, by='text', name="Пароль и безопасность", wait=wait)
    findElem(driver, by='text', name="Пароли для внешних приложений", wait=wait)
    findElem(driver, by='text', name="Добавить", wait=wait)
    name = gen('name')
    findElem(driver, by='name', name="name", text=name, wait=wait, sleep=True, send=True)
    findElem(driver, by='name', name="password", text=ac_password, wait=wait, sleep=True, send=True)

    # RuCaptcha.solve_v2(driver)
    time.sleep(45)

    findElem(driver, by='text', name="Продолжить", wait=wait)
    time.sleep(2)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, f"div.view_dialog__password")))
    return str(driver.find_element(By.CSS_SELECTOR, f"div.view_dialog__password").text).replace('\n', '')

def register_sel(driver, url, wait=5.0):
    driver.get(url)

    domain = gen('domain')
    password = gen('password')
    value = f"{domain}@mail.ru:{password}"
    findElem(driver, by='name', text=gen('name'), name="fname", wait=wait, sleep=True)
    findElem(driver, by='name', text=gen('name'), name="lname", wait=wait, sleep=True)
    findElem(driver, by='text', name="День", wait=wait, sleep=True)
    findElem(driver, by='text', name=gen('R'), wait=wait, sleep=True)
    findElem(driver, by='text', name="Месяц", wait=wait, sleep=True)
    findElem(driver, by='text', name=gen('month'), wait=wait, sleep=True)
    findElem(driver, by='text', name='Год', wait=wait, sleep=True)
    findElem(driver, by='text', name=gen('year'), wait=wait, sleep=True)
    findElem(driver, by='text', name=gen('gender'), wait=wait, sleep=True)
    findElem(driver, by='name', name="username", text=domain, wait=wait, sleep=True, send=True)
    findElem(driver, by='name', name="password", text=password, wait=wait, sleep=True, send=True)
    findElem(driver, by='name', name="repeatPassword", text=password, wait=wait, sleep=True, send=True)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.styles-mobile__captchaImage--sHzh3")))

    for cycle in range(3):
        answer = RuCaptcha.solve_text(driver)
        findElem(driver, by='placeholder', name="Код", text=answer, wait=wait, sleep=True)
        driver.find_element(By.XPATH, f"//input[@placeholder='Код']").send_keys(Keys.ENTER)

        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//*[text() = 'Настроить']")))
            welcome_page(driver, wait)
            time.sleep(2)
            return value
        except: pass

def log_in_sel(driver, url, mail, password, wait=5):
    driver.get(url)

    findElem(driver, by='name', name="username", text=mail, wait=wait, sleep=True, send=True)
    time.sleep(wait / 10)
    findElem(driver, by='name', name="password", text=password, wait=wait, sleep=True, send=True)

boxes = ["Inbox", '"&BB4EQgQ,BEAEMAQyBDsENQQ9BD0ESwQ1-"', '"&BCEEPwQwBDw-"', '"INBOX/Newsletters"']

def delete_all(address, imap_pas, p=0):
    global boxes
    imap = IMAP4_SSL('imap.mail.ru')
    try:
        imap.login(address, imap_pas)
    except:
        print(f'Shit {p}')
        return

    for box in boxes:
        imap.select(box)

        _, data = imap.search(None, 'ALL')

        for num in data[0].split():
            imap.store(num, "+FLAGS", "\\Deleted")
        try:
            imap.expange()
        except: pass

    imap.close()
    imap.logout()

def find_from(address, imap_pas, from_ad, p=0):
    imap = IMAP4_SSL('imap.mail.ru')
    try:
        imap.login(address, imap_pas)
    except:
        print(f'Shit {p}')
        return []

    global boxes
    res = []

    for box in boxes:
        imap.select(box)
        _, msum = imap.search(None, 'ALL')

        for num in msum[0].split():
            _, data = imap.fetch(num, "(RFC822)")

            message = email.message_from_bytes(data[0][1])

            if from_ad in message.get('From'):
                res.append(num)

    imap.close()
    imap.logout()
    return res

def find_by_key(address, imap_pas, key, p=0):
    imap = IMAP4_SSL('imap.mail.ru')
    try:
        imap.login(address, imap_pas)
    except:
        print(f'Shit {p}')
        return []

    global boxes
    res = []
    key = key.lower()

    for box in boxes:
        imap.select(box)
        _, msum = imap.search(None, 'ALL')

        for num in msum[0].split():
            _, data = imap.fetch(num, "(RFC822)")

            message = email.message_from_bytes(data[0][1])

            rem = 0
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    if key in part.as_string().lower():
                        rem = 1
                        break

            if rem == 1 or key in message.get('From').lower() or key in message.get('Subject').lower():
                res.append(num)

    imap.close()
    imap.logout()
    return res

def find_new(address, imap_pas, p=0):
    imap = IMAP4_SSL('imap.mail.ru')
    try:
        imap.login(address, imap_pas)
    except:
        print(f'Shit {p}')
        return []

    global boxes
    res = []

    for box in boxes:
        imap.select(box)
        _, msum = imap.search(None, 'ALL')

        for num in msum[0].split():
            res.append(num)

    imap.close()
    imap.logout()
    return res
