# import sys
import time
import threading
from bs4 import BeautifulSoup
# from fontTools.designspaceLib.types import clamp
from playwright.sync_api import sync_playwright

def amazon_page(page):
    pass

def flipkart_page(page):
    page.goto('https://www.flipkart.com')
    product_name = input("Enter product:")
    page.fill('.Pke_EE', product_name)
    page.press('._2iLD__', 'Enter')
    soap = BeautifulSoup(page.inner_html('.DOjaWF'), features='lxml')
    products = soap.find_all('div', class_='tUxRFH')
    # print(products)
    print("length: ", len(products))
    if len(products) == 0:
        products = soap.find_all('div', class_='_1sdMkc LFEi7Z')
        for i in products:
            print("name: ", i.find('div', class_='hCKiGj').a.text)
            print("price: ", i.find('div', class_='Nx9bqj').text)
            print()
    else:
        for i in products:
            print("name: ", i.find('div', class_='KzDlHZ').text)
            print("price: ", i.find('div', class_='Nx9bqj _4b5DiR').text)
            print("rating: ", i.find('div', class_='XQDdHH').text)
            print()

if __name__ == '__main__':
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,slow_mo=50)
        f_page = browser.new_page()
        # a_page = browser.new_page()

        # threading.Thread(target=flipkart_page,args=(f_page,))
        flipkart_page(f_page)
        # a_page.goto('https://www.amazon.com')
        # product_name = input("Enter product:")
        # a_page.fill('#twotabsearchtextbox', product_name)
        # a_page.press('#nav-search-submit-button', 'Enter')

        time.sleep(5)
        browser.close()