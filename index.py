import requests
from flask import Flask,render_template, request, jsonify, json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def scrape_flipkart(product_name):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False,slow_mo=50)
        page = browser.new_page()
        page.route("**/*", lambda route: route.abort() if route.request.resource_type in ['image', 'stylesheet', 'font'] else route.continue_())
        page.goto('https://www.flipkart.com',timeout=60000)
        page.fill('.Pke_EE', product_name)
        page.press('._2iLD__', 'Enter')
        soap = BeautifulSoup(page.inner_html('.DOjaWF'), features='lxml')
        products = soap.find_all('div', class_='tUxRFH')[:10]
        # print(products)
        print("length: ", len(products))

        # price = []
        # rating = []
        # names = []
        # links = []
        # images_ = []

        flipkart = []

        if len(products) == 0:
            products = soap.find_all('div', class_='_1sdMkc LFEi7Z')[:10]
            for i in products:
                obj = {'name': i.find('div', class_='hCKiGj').text,
                       'price': i.find('div', class_='Nx9bqj').text,
                       'image': '#',
                       'link': '#'}
                flipkart.append(obj)
                # names.append(i.find('div', class_='hCKiGj').a.text)
                # price.append(i.find('div', class_='Nx9bqj').text)
                # rating.append("none")
        else:
            for i in products:
                obj = {'name': i.find('div', class_='KzDlHZ').text,
                       'price': i.find('div', class_='Nx9bqj _4b5DiR').text,
                       'image': i.find('img', class_='DByuf4').get('src'),
                       'link': 'https://www.flipkart.com' + i.a.get('href')}
                flipkart.append(obj)
                # names.append(i.find('div', class_='KzDlHZ').text)
                # price.append(i.find('div', class_='Nx9bqj _4b5DiR').text)
                # images_.append(i.find('img', class_='DByuf4').get('src'))
                # links.append('https://www.flipkart.com' + i.a.get('href'))
                # rating.append(i.find('div', class_='XQDdHH').text)
        return flipkart


def scrape_amazon(product_name):
    URL = 'https://www.amazon.in/s?k=' + product_name
    response = requests.get(URL)
    iter = 15
    while response.status_code == 503 and iter != 0:
        print(iter)
        response = requests.get(URL)
        iter -= 1

    soap = BeautifulSoup(response.text, 'lxml')

    products = soap.find_all('div',
                             class_='puisg-col puisg-col-4-of-12 puisg-col-8-of-16 puisg-col-12-of-20 puisg-col-12-of-24 puis-list-col-right')[:10]
    images = soap.find_all('div',
                           class_='puisg-col puisg-col-4-of-12 puisg-col-4-of-16 puisg-col-4-of-20 puisg-col-4-of-24 puis-list-col-left')[:10]
    print("prod:",len(products))
    print("prod:",len(images))
    total_prod = min(len(products), len(images))
    print("total: ",total_prod)
    names = []
    _prices = []
    _images = []
    links_ = []

    amazon = []

    for i in range(total_prod):

        name = products[i].h2
        link = products[i].h2.a
        price = products[i].find('span', class_='a-price-whole')
        image = images[i].find('img', class_='s-image')

        obj = {
            'name':name.text if name else 'Name not available',
            'link':'https://www.amazon.in' +  link.get('href') if link else '#',
            'image':image.get('src') if image else '#',
            'price':price.text if price else 'not available'
        }

        amazon.append(obj)
        # links_.append('https://www.amazon.com' +  link.get('href') if link else '#')
        # names.append(name.text if name else 'Name not available'),
        # _prices.append(price.text if price else 'Price not available')
        # _images.append(image.get('src') if image else '#')

    return amazon


@app.post('/compare')
def compare_prices():
    product_name = request.json['product']
    print(product_name)
    if not product_name:
        return json.dumps({"error":"server error"})

    flipkart_data = scrape_flipkart(product_name)
    amazon_data = scrape_amazon(product_name)

    results = {}
    if flipkart_data:
        print(flipkart_data)
        results['flipkart'] = flipkart_data
    if amazon_data:
        print(amazon_data)
        results['amazon'] = amazon_data

    # print(results)

    if results:
        return json.dumps(results)
    else:
        return json.dumps({'error':'error server'})

@app.get('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
