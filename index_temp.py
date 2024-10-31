import time

import requests
from flask import Flask,render_template, request, jsonify, json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

app = Flask(__name__)


def scrape_flipkart(page, product_name):
        page.goto('https://www.flipkart.com',timeout=60000)
        page.fill('.Pke_EE', product_name)
        page.press('._2iLD__', 'Enter')
        soap = BeautifulSoup(page.inner_html('.DOjaWF'), features='lxml')
        products = soap.find_all('div', class_='tUxRFH')
        # print(products)
        print("length: ", len(products))

        price = []
        rating = []
        names = []

        if len(products) == 0:
            products = soap.find_all('div', class_='_1sdMkc LFEi7Z')
            for i in products:
                names.append(i.find('div', class_='hCKiGj').a.text)
                price.append(i.find('div', class_='Nx9bqj').text)
                rating.append("none")
        else:
            for i in products:
                names.append(i.find('div', class_='KzDlHZ').text)
                price.append(i.find('div', class_='Nx9bqj _4b5DiR').text)
                rating.append(i.find('div', class_='XQDdHH').text)
        return {'website': 'Flipkart','name':names, 'price': price, 'rating': rating, 'free_delivery': 'Yes',
                'offers': 'Exchange Offers'}


def scrape_amazon(page,product_name):
    page.goto('https://www.amazon.com', timeout=600000)
    # while True:
    #     time.sleep(300)
    # page.locator("text='Search Amazon.in'").fill(product_name)
    page.fill('#twotabsearchtextbox', product_name)
    page.press('#nav-search-submit-button', 'Enter')
    # page.inner_html
    # page.wait_for_selector('span[data-component-type="s-result-info-bar"][data-component-id="31"]')
    # span_element = page.locator('span[data-component-type="s-result-info-bar"][data-component-id="31"]')
    # print("count:",span_element.count())
    print(page.inner_html('#search'))
    soap = BeautifulSoup(page.inner_html('#search'), 'lxml')
    # print(soap)
    products = soap.find_all('div',
                             class_='puisg-col puisg-col-4-of-12 puisg-col-8-of-16 puisg-col-12-of-20 puisg-col-12-of-24 puis-list-col-right')
    images = soap.find_all('div',
                           class_='puisg-col puisg-col-4-of-12 puisg-col-4-of-16 puisg-col-4-of-20 puisg-col-4-of-24 puis-list-col-left')
    print("prod:",len(products))
    print("img:",len(images))
    total_prod = min(len(products), len(images))
    print("total: ",total_prod)
    names = []
    price = []
    image = []
    for i in range(total_prod):
        name = products[i].h2
        price = products[i].find('span', class_='a-price-whole')
        image = images[i].find('img', class_='s-image')

        names.append(name.text if name else 'Name not available'),
        price.append(price.text if price else 'Price not available')
        image.append(image.get('src') if image else 'Image not available')

    return {
            'website':'amazon',
            'name': names,
            'price': price,
            'image': image
        }


@app.post('/compare')
def compare_prices():
    product_name = request.json['product']
    print(product_name)
    if not product_name:
        return jsonify({'error': 'No product specified'}), 400

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        # page.route("**/*", lambda route: route.abort() if route.request.resource_type in ['image', 'stylesheet',
        #                                                                                   'font'] else route.continue_())

        flipkart_data = scrape_flipkart(page, product_name)
        amazon_data = scrape_amazon(page, product_name)
        browser.close()

        results = []
        if flipkart_data:
            print(flipkart_data)
            results.append(flipkart_data)
        if amazon_data:
            print(amazon_data)
            results.append(amazon_data)

        # print(results)

        if results:
            return jsonify(results)
        else:
            return jsonify({'error': 'No products found'}), 404

@app.get('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
