#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import urllib2
from bs4 import BeautifulSoup


flowers = ['stephanotis', 'pansy', 'marigold', 'stock', 'lotus', 'dahlia', 'gladioli', 'chrysanthemum', 'apple blossom', 'camellia', 'sweet pea', 'lavender', 'ranunculus', 'statice', 'protea', "queen anne's lace", 'poinsettia', 'snapdragons', 'lisianthus', 'freesia', 'delphinium', 'bourvardia', 'aster', 'bird of paradise', 'heather', 'anthurium', 'anemomne', 'crocus', 'amaryllis', 'alstromeria', 'cypress', 'hibiscus', 'morning glory', 'laurel', 'dianthus', 'canna', 'snapdragon', 'oriental poppy', "parrot's beak", 'bleeding heart', 'jade vine']


def get_html(url):
    headers = {}
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    return response.read()


def get_image_urls(html):
    found_img_urls = []
    soup = BeautifulSoup(html, 'lxml')
    img_urls = soup.find_all('img', {'class': 'rg_i'})
    for url in img_urls:
        if url.get('data-src'):
            found_img_urls.append(url['data-src'])
    return found_img_urls


def main():
    image_folder = 'flower_images'
    if not os.path.isdir(image_folder):
        os.mkdir(image_folder)

    i = 0
    while i < len(flowers):
        items = []
        flower = flowers[i]
        search_string = flowers[i].replace(' ','%20')
        
        if not os.path.isdir('{}/{}'.format(image_folder, flower)):
            os.mkdir('{}/{}'.format(image_folder, flower))

        url = 'https://www.google.com/search?q=' + search_string + '&source=lnms&tbm=isch&sa=X&ved=0ahUKEwiYiNyJ-JvYAhUNzWMKHbcdBvoQ_AUICigB&biw=1680&bih=949'
        html =  get_html(url)
        img_urls = get_image_urls(html=html)

        img_no = 0
        while img_no < len(img_urls):        
            try:
                req = urllib2.Request(img_urls[img_no])
                response = urllib2.urlopen(req,None,15)
                output_file = open('{}/{}/{}.jpg'.format(image_folder, flower, str(img_no + 1)), mode='wb')
                data = response.read()
                output_file.write(data)
                response.close();
                img_no += 1
            except urllib2.HTTPError as e:
                img_no += 1
            except urllib2.URLError as e:
                img_no += 1
            except IOError:
                img_no += 1

        i += 1

if __name__ == '__main__':
    main()