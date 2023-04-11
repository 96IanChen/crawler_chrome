from django.shortcuts import render, redirect
from web.models import Div, Text
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

# Create your views here.

def home(request):
    #---
    #---
    return render(request, "home.html", locals())

def crawler(request):
    #key = 'a51'
    count = 1
    datatype = ''
    keyword = ''
    counts = ''
    datatype = request.POST.get('DataType', '')
    keyword = request.POST.get('KeyWord', '')
    counts = request.POST.get('Counts', '')

    while True:
    #for i in range(3):
        options = Options()
        options.add_argument("--disable-notifications")
        
        chrome = webdriver.Chrome('C:\\Users\ian\Desktop\crawler_chrome\chromedriver', chrome_options=options)
        chrome.get("https://shopee.tw/")
        time.sleep(3)
        chrome.maximize_window()

        # 尋找網頁中的搜尋框
        inputElement = chrome.find_element_by_class_name("shopee-searchbar-input__input")

        # 在搜尋框中輸入文字
        inputElement.send_keys(keyword+Keys.ENTER)

        #chrome.get("https://shopee.tw/search?keyword=a51")
        chrome.get("https://shopee.tw/search?keyword="+keyword)
        time.sleep(5)

        soup = BeautifulSoup(chrome.page_source, 'html.parser')

        # datatype:div
        # keyword:col-xs-2-4 shopee-search-item-result__item 
        # counts:int(counts)

        titles = soup.find_all(datatype, {
            'class': 'col-xs-2-4 shopee-search-item-result__item'}, limit=int(counts))

        #titles = soup.find_all('div', {
            #'class': 'col-xs-2-4 shopee-search-item-result__item'}, limit=5)

        for title in titles:
            
            dit = str(title)
            div = Div(content=dit, divnumber=count)
            div.save()

            post = title.find('div', {'class': 'ie3A+n bM+7UW Cve6sh'})
        
            if post:
                textpr = post.getText()
                text = Text(content=textpr, div=div)
                text.save()
                print(post.getText())
            count += 1
        chrome.close()

        time.sleep(1800)
    #chrome.quit()
    return redirect("/home/")
    #return render(request, "crawler.html", locals())

#------------------------------------------------------------------
dlist = []

def divlist(request):
    divs = Div.objects.all().order_by('id')
    return render(request, 'divlist.html', locals())

def result(request, divid=None):
    global dlist
    dlist = []
    div = Div.objects.get(id=divid)
    did = div.id
    dlist.append(did)
    texts = Text.objects.filter(div=div)
    return render(request, 'result.html', locals())

def delete(request, divid=None):
    global dlist
    did = dlist[0]
    div = Div.objects.get(id=did)
    return render(request, 'delete.html', locals())

def enddelete(request):
    global dlist
    did = dlist[0]
    div = Div.objects.get(id=did)
    texts = Text.objects.filter(div=div)
    for text in texts:
        text.div = None
        text.delete()
    div.delete()
    return render(request, 'enddelete.html', locals())