# git clone this repo https://github.com/Naveen142005/natureworld
# to get the static html files in here!

import re
import csv
from bs4 import BeautifulSoup as bs

def parse_sub_page(table,path):
    with open(path,'r') as file:
        soup = bs(file,features='lxml')
    creature = soup.find('span',id='creatureName').text.strip()
    ptags = [i.text for i in soup.find_all('p')]

    table.writerow([creature]+[int(ptags[i]) for i in range(1,len(ptags)-1,2)])

if __name__ == '__main__':
    with open('./natureworld/index.html','r') as file:
        soup = bs(file,features='lxml')

    # print(soup)
    full = soup.find('div',class_='full')
    nw = ''.join([i.text for i in full.find('span').find_all('span')])

    cards = full.find('div',class_='card-full').find_all('div',class_='card_1')

    cardsData = [[i.h1.text,re.sub(r'\s\s+','',i.span.text)] for i in cards]

    second = full.find_all('div',class_='water_fall_about')
    secondData = [re.sub(r'\s\s+','',i.text.strip()) for i in second]

    with open('./static_data.csv','w',newline='') as file:
        file_writer = csv.writer(file)
        file_writer.writerow(['Creatures','Species','Photos','Extinct','Names'])
        parse_sub_page(file_writer,'./natureworld/brids.html')
        parse_sub_page(file_writer,'./natureworld/butterfly.html')
        parse_sub_page(file_writer,'./natureworld/fish.html')
        parse_sub_page(file_writer,'./natureworld/frog.html')
        parse_sub_page(file_writer,'./natureworld/pengun.html')
        parse_sub_page(file_writer,'./natureworld/rabit.html')
        parse_sub_page(file_writer,'./natureworld/tiger.html')
    print(cardsData)
    print(secondData)
    print(nw)