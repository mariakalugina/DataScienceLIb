from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pprint import pprint
from pymongo import MongoClient

import time

driver = webdriver.Chrome()
driver.get("https://account.mail.ru/login?from=main&split=mainbtn")
login = 'study.ai_172@mail.ru'
password = 'NextPassword172'
time.sleep(3)
element_login = driver.find_element_by_name('username')
element_login.send_keys(login)
time.sleep(2)
element_login.send_keys(Keys.ENTER)
element_pass = driver.find_element_by_name('password')
time.sleep(2)
element_pass.send_keys(password)
element_pass.send_keys(Keys.ENTER)

#   ящик открылся
time.sleep(10)
link_lists = []
mumber_of_letters = 0
while True:
    mail_items = driver.find_elements_by_xpath('//a[@data-id]')
    for item in mail_items:
        link = item.get_property('href')
        link_lists.append(link)
    link_lists = list(set(link_lists))

    if mumber_of_letters == len(mail_items):
        break
    else:
        mumber_of_letters = len(mail_items)
    down = mail_items[-1].send_keys(Keys.PAGE_DOWN)

pprint(link_lists)
pprint(len(link_lists))



letters = []
for link in link_lists:
    driver.get(link)
    time.sleep(4)
    from_element = driver.find_element_by_class_name('letter-contact')
    subject_element = driver.find_element_by_class_name('thread__subject')
    time_element = driver.find_element_by_class_name('letter__date')
    text_element = driver.find_element_by_class_name('letter-body__body-content')
    time.sleep(2)

    letter = {}
    letter['from'] = from_element.text
    letter['subject'] = subject_element.text
    letter['text'] = text_element.text
    letter['time'] = time_element.text
    letters.append(letter)

pprint(letters)
driver.close()

#сохраняем письма в базу данных
client = MongoClient('localhost', 27017)
db = client['mail-ru']
collection = db.test_collection
collection.insertMany(letters)