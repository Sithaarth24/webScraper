import re
import csv
import requests
from bs4 import BeautifulSoup as bs
import os
from pyexpat import features

def parse_product_page(url,c):
    response = requests.get(url)
    soap = bs(response.text,features='lxml')
    try:
        title = soap.find('span',id='productTitle').text.strip()
        print(title)
    except:
        print('page not found')


if __name__ == '__main__':
    soap = None
    # if os.path.isfile('./amazon.html'):
    #     with open('amazon.html','r') as file:
    #         print('present')
    #         soap = bs(file,features='lxml')
    # else:
    inp = input("Enter product:").replace(' ','+')
    var = False
    URL = 'https://www.amazon.in/s?k=' + inp
    response = requests.get(URL)
    iter = 10
    while response.status_code == 503 and iter != 0:
        print(iter)
        response = requests.get(URL)
        iter-=1

    print(response.status_code)

    soap = bs(response.text,features='lxml')

    products = soap.find_all('div',class_ = 'puisg-col puisg-col-4-of-12 puisg-col-8-of-16 puisg-col-12-of-20 puisg-col-12-of-24 puis-list-col-right')
    images = soap.find_all('div',class_ = 'puisg-col puisg-col-4-of-12 puisg-col-4-of-16 puisg-col-4-of-20 puisg-col-4-of-24 puis-list-col-left')
    # print(products)
    print(len(products))
    print(len(images))

    total_prod = min(len(products), len(images))

    for i in range(total_prod):
        name = products[i].h2
        price = products[i].find('span',class_= 'a-price-whole')
        image = images[i].find('img', class_='s-image')

        if image: print("image: ",type(image.get('src')))
        else: print("image: not available")

        if name: print("name: ", name.text)
        else: print("name: not available")

        if price: print("price: ", price.text)
        else: print("name: not available")

        print()

    # link_tags = soap.find_all('a',class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
    # for i,l in enumerate(link_tags):
    #     parse_product_page('https://www.amazon.in/'+l['href'],i)

    # if var:
    #     with open('./natureworld/index.html', 'r') as file:
    #         soup = bs(file, features='lxml')
    #
    #     # print(soup)
    #     full = soup.find('div', class_='full')
    #     nw = ''.join([i.text for i in full.find('span').find_all('span')])
    #
    #     cards = full.find('div', class_='card-full').find_all('div', class_='card_1')
    #
    #     cardsData = [[i.h1.text, re.sub(r'\s\s+', '', i.span.text)] for i in cards]
    #
    #     second = full.find_all('div', class_='water_fall_about')
    #     secondData = [re.sub(r'\s\s+', '', i.text.strip()) for i in second]
    #     with open('./static_data.csv', 'w', newline='') as file:
    #         file_writer = csv.writer(file)
    #         file_writer.writerow(['Creatures', 'Species', 'Photos', 'Extinct', 'Names'])
    #     print(cardsData)
    #     print(secondData)
    #     print(nw)
    #     full = soup.find('div', class_='full')
    #     nw = ''.join([i.text for i in full.find('span').find_all('span')])
    #
    #     cards = full.find('div', class_='card-full').find_all('div', class_='card_1')
    #
    #     cardsData = [[i.h1.text, re.sub(r'\s\s+', '', i.span.text)] for i in cards]
    #
    #     second = full.find_all('div', class_='water_fall_about')
    #     secondData = [re.sub(r'\s\s+', '', i.text.strip()) for i in second]
    #     with open('./static_data.csv', 'w', newline='') as file:
    #         file_writer = csv.writer(file)
    #         file_writer.writerow(['Creatures', 'Species', 'Photos', 'Extinct', 'Names'])