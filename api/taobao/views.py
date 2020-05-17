from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup
from selenium import webdriver
from os.path import dirname, abspath
import requests
import os
import json

URL = "https://item.taobao.com/item.htm?id="

@api_view(['GET'])
def get_product(request):
    info = {}

    chrome_dir = dirname(dirname(abspath(__file__))) + "/chromedriver"
    custom_options = webdriver.ChromeOptions()
    prefs = {
    "translate_whitelists": {"zh-CN":"ko"},
    "translate":{"enabled":"true"}
    }
    custom_options.add_experimental_option("prefs", prefs)
    driver=webdriver.Chrome(chrome_dir, options=custom_options)
    driver.implicitly_wait(3)
    product_url =URL + request.query_params['id']
    driver.get(product_url)
    try :
        driver.switch_to_alert().accept()
    except:
        pass

    _html = driver.page_source
    soup = BeautifulSoup(_html, 'html.parser')
    title_tag = soup.find(id="J_Title")
    info["title"] = title_tag.h3.text.lstrip('\n').rstrip('\n').strip()
    info["price"] = soup.find(class_="tb-rmb-num").text
    info["options"] = []
    options = []
    option_tags = soup.find_all("dl", class_="J_Prop")
    for option_tag in option_tags:
        
        option_name = option_tag.dt.text
        option_dict = {option_name: []}
        for li in option_tag.dd.ul.findAll('li'):
            option_dict[option_name].append(li.a.text.lstrip('\n').rstrip('\n').strip())
        options.append(option_dict)
    info["options"] = options
    driver.close()
    info_json = json.dumps(info)
    return HttpResponse(info_json)
