from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import re
from apartment import apartmentAd, export_apartment, new_apartment
from datetime import datetime, timedelta
import csv


def stringFormat(s):
    """
    Remove whitespaces, dashes from the string and also make it lowercase
    :param s: str, the string from which we would like to remove or change characters
    :return: s, str, the reformatted string
    """
    s = s.replace(" ", "")
    s = s.replace("-","")
    s = s.lower()
    return s

def timestamp_transform(timestamp):
    """
    Transforming the relative timestamp (ex. "godzinę temu") from the gumtree website to absolute time.
    :param timestamp: str, the relative timestamp from the gumtree website
    :return: str, the absolute time when the ad was posted in the form "YYYY-MM-DD HH:MM"
    """
    if timestamp == 'godzinę temu':
        return (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M')
    timestamp=int(re.sub('\D', '', timestamp))
    return (datetime.now() - timedelta(hours=timestamp)).strftime('%Y-%m-%d %H:%M')

def filter_kawalerka(title):
    """
    filtering out ads with the "kawalerka" phrase in the title.
    :param title: str containing ad title
    :return: bool: 1 if the ad is acceptable, 0 if the ad is not acceptable
    """
    if (title.lower()).find('kawalerka') < 0:
        return 1
    else:
        print('kawalerka: ', title)
        return 0

def filter_2pokojeOLD(title):
    """
    filtering out ads with the "2 pokoje" phrase in the title.
    :param title: str containing ad title
    :return: bool: 1 if the ad is acceptable, 0 if the ad is not acceptable
    """
    if (title.lower()).find('2 pokoje') < 0:
        return 1
    else:
        print('2 pokoje: ', title)
        return 0

def filter_2pokoje(title):
    """
    filtering out ads with the "2 pokoje" phrase in the title.
    :param title: str containing ad title
    :return: bool: 1 if the ad is acceptable, 0 if the ad is not acceptable
    """
    s = title.lower()
    if ((s.find('2 pokoje') < 0) and (s.find('dwa pokoje') < 0) and (s.find('dwupokojowe') < 0)):
        return 1
    else:
        print('2 pokoje: ', title)
        return 0

def filter_area_title(title, min_area):
    """
    filtering out ads with the area above min_area treshold
    :param title: str containing ad title
            min_area: int, minimum area of the apartment
    :return: bool: 1 if the ad is acceptable, 0 if the ad is not acceptable
    """
    s = title.lower()
    s = s.replace(',', '.')
    i1 = s.find('m2')
    #print('i1: ', i1)
    # Check if there is a 'm2' phrase, if not, accept
    if i1 <= 0:
        #print('i1<=0')
        return 1
    # Check if there is a "space" between smth and "m2" characters and remove it
    while s[i1-1] == ' ' and i1 >= 1:
        s = s[:i1-1] + s[i1:]
        i1 = i1 - 1
    #print('space removed: ', s)
    # Check if the symbol before "m2" is a digit, if not, accept
    if not s[i1-1].isdigit():
        return 1
    i0 = i1-1
    #print("i0 before loop: ", i0)
    #print('s[i0]: ', s[i0])
    while i0 > 0 and (s[i0].isdigit() or s[i0] == '.'): # if the title had a float number apartment size, we iterate over "." also
        #print('while loop!')
        i0 = i0 - 1
    size = float(s[i0+1:i1])
    #print('s[i0+1]', s[i0+1])
    #print('s[i1-1]', s[i1 - 1])
    #print(size)
    if size >= min_area:
        return 1
    else:
        print('Too small: ', title)
        return 0

def old_apartment_timestamp(timestamp):
    """
    The script to find if the ads were posted longer than 24 hours from the moment the script is run.
    :param timestamp: str, the relative timestamp from the gumtree website
    :return: bool, 1 if the ad is older than 24 hours, 0 if it is not
    """
    return (timestamp.find('godzin') < 0 and timestamp.find('minut') < 0 and timestamp.find('sekund') < 0)


def olxURLgenerator(district = "ochota", priceA=0, priceB=1000000, areaA=0, areaB=200):
    """
    A script to generate a URL for olx.pl apartments deals, with parameters set
    according to function arguments

    returns:
    (str) with URL

    arguments:
    district (str) - the name of the district, no polish special characters allowed
    priceA (int) - show apartments of a price above ...
    priceB (int) - show apartments of a price below ...
    areaA (int) - show apartments of a size above ...
    areaB (int) - show apartments of a size below ...
    """

    tURL = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/warszawa/?"
    searchExpressions = ["search[district_id]=", "search[filter_float_price%3Afrom]=", "search[filter_float_price%3Ato]=", "search[filter_float_m%3Afrom]=", "search[filter_float_m%3Ato]="]

    district = stringFormat(district)
    #print(district)
    districts = {"ochota" : 355, "wola" : 359, "pragapoludnie" : 381, "pragapolnoc" : 379, "bemowo" : 367, "ursus" : 371, "wlochy" : 357, "wilanow" : 375, "wesola" : 533, "wawer" : 383, "ursynow" : 373, "targowek" : 377, "bialoleka" : 365, "srodmiescie" : 351, "rembertow" : 361, "mokotow" : 353, "bielany" : 369, "zoliborz" : 363}

    parameterValues = [districts[district], priceA, priceB, areaA, areaB]
    parametersChanged = [district!='ochota', priceA !=0, priceB != 1000000, areaA != 0, areaB != 200]
    isParametersChanged = (sum(parametersChanged)!=0)

    for i in range(len(parametersChanged)):
        print(i)
        if parametersChanged[i]:
            tURL = tURL + searchExpressions[i] + str(parameterValues[i]) + "&"
        print(searchExpressions[i])

    return tURL

def gumtreeURLgenerator(district='praga-poludnie', priceA=0, priceB=550000, page = 1):
    """
    The script generates URL for the ads meeting particular criteria.
    :param district: str, the district from which the ads are to be found
    :param priceA: int, the minimum price of the apartment
    :param priceB: int, the maximum price of the apartment
    :param page: int, results page number
    :return: str, URL for the gumtree search
    """
    baseURL = 'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/'
    if district == 'praga-poludnie':
        code = '/v1c9073l3200015p'
    elif district == 'bielany':
        code = '/v1c9073l3200011p'
    middleURL = '/page-'+ str(page) + code + str(page)
    searchParameters = '?pr=' + str(priceA) + ',' + str(priceB)
    return baseURL + district + middleURL + searchParameters


def getWebsite(URL):
    """
    Download website from the given URL
    :param URL: str, the URL of the website
    :return: str, the downloaded website
    """
    req = Request(URL)
    try:
        response = urlopen(req)
    except HTTPError as e:
        print('Error code: ', e.code)
        return 0
    except URLError as e:
        print('Reason: ', e.reason)
        return 0
    else:
        print('Website accessible!')
    website = urlopen(URL).read()
    #print(website)
    return website


def scraperGumtree(page, csvname):
    """
    The main gumtree scraper. Takes a gumtree website, locates apartment ads, analyses them and exports to the database
    :param page: the website we are to scrape
    :param csvname: str, name of the database csv file
    :return: nothing is returned, but on the way the script exports data to database
    """
    soup = BeautifulSoup(page, 'html.parser')
    Ad_list = soup.find(class_="view")
    Ad_list_items = Ad_list.find_all(class_="tileV1") # list of the ads
    #print('----------------------')
    #print('----------------------')
    #print(Ad_list_items[0])
    for ad in Ad_list_items:
        title = ad.find("a").contents[0]
        link = 'https://www.gumtree.pl'+ad.find("a")['href']
        timestamp = ad.find(class_="creation-date").findChildren("span", recursive=False)[0].contents[0]
        if old_apartment_timestamp(timestamp):
            print('Reached the old ads!')
            return 0
        price = ad.find(class_="ad-price").contents[0].replace('zł','')
        price = int(re.sub('[\W_]+', '', price))
        tmpapartment = apartmentAd(price = price, title = title, URL = link, timestamp = timestamp_transform(timestamp))
        if new_apartment(tmpapartment, csvname) and filter_kawalerka(title) and filter_2pokoje(title) and filter_area_title(title, 52):
            #print('Exporting to:', csvname)
            export_apartment(tmpapartment, csvname)
    return 1