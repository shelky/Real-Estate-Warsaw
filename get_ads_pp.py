#!/usr/bin/python3

from WSscripts import *

i = 1
page_number = 1
while i:
    url = gumtreeURLgenerator(district='praga-poludnie', priceA=0, priceB=550000, page = page_number)
    #print(url)
    print("Page number: ", page_number)
    #print('----------------------')
    #print(url)
    #print('----------------------')
    page = getWebsite(url)
    i = scraperGumtree(page, 'apartments_praga_poludnie.csv')
    page_number = page_number + 1