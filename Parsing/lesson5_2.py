from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pprint import pprint
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import time

driver = webdriver.Chrome()
driver.get("https://www.mvideo.ru")
#time.sleep(15)
goods_number = 0
goods_elements = set()
while True:
    time.sleep(15)
    hits_element = driver.find_element_by_xpath('//div[contains(text(),"Хиты продаж")][1]/../../..')
    next_button = hits_element.find_element_by_xpath('//a[contains(@class,"next-btn")]')

    #получаем список элементов, содержащих в себе товары
    new_goods_elements= hits_element.find_elements_by_xpath('//div/ul/li/div/div/div/div//a[@data-product-info]')
    pass
    for new_element in new_goods_elements:
        goods_elements.add(new_element)
    if (len(goods_elements)==goods_number):
        break
    else:
        goods_number=len(goods_elements)
        next_button.click()
print(len(goods_elements))
items = []
for good in goods_elements:
    try:
        item={}

        item['link'] = good.get_property('href')
        info = good.get_attribute('data-product-info')
        info = eval(info)
        try:
            item['name'] = info['productName']
            item['price'] = info['productPriceLocal']
            items.append(item)
        except:
            pass
    except :
        pass
pprint(items)
print(len(items))
driver.close()
