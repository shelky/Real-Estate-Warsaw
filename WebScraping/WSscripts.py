from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def stringFormat(s):
    """
    Remove whitespaces, dashes from the string and also make it lowercase

    :param s:
    :return: s
    """
    s = s.replace(" ", "")
    s = s.replace("-", "")
    s = s.lower()
    return s


def gumtreeURLgenerator(district='praga-poludnie', priceA=0, priceB=550000):
    baseURL = 'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/'
    middleURL = '/v1c9073l3200015p1'
    searchParameters = '?pr=' + str(priceA) + ',' + str(priceB)
    return baseURL + district + middleURL + searchParameters


def olxURLgenerator(district="ochota", priceA=0, priceB=1000000, areaA=0, areaB=200):
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
    searchExpressions = ["search[district_id]=", "search[filter_float_price%3Afrom]=",
                         "search[filter_float_price%3Ato]=", "search[filter_float_m%3Afrom]=",
                         "search[filter_float_m%3Ato]="]

    district = stringFormat(district)
    print(district)
    districts = {"ochota": 355, "wola": 359, "pragapoludnie": 381, "pragapolnoc": 379, "bemowo": 367, "ursus": 371,
                 "wlochy": 357, "wilanow": 375, "wesola": 533, "wawer": 383, "ursynow": 373, "targowek": 377,
                 "bialoleka": 365, "srodmiescie": 351, "rembertow": 361, "mokotow": 353, "bielany": 369,
                 "zoliborz": 363}

    parameterValues = [districts[district], priceA, priceB, areaA, areaB]
    parametersChanged = [district != 'ochota', priceA != 0, priceB != 1000000, areaA != 0, areaB != 200]
    isParametersChanged = (sum(parametersChanged) != 0)

    for i in range(len(parametersChanged)):
        print(i)
        if parametersChanged[i]:
            tURL = tURL + searchExpressions[i] + str(parameterValues[i]) + "&"
        print(searchExpressions[i])

    return tURL


def getWebsite(URL):
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
    print(website)
    return website


print(olxURLgenerator(district='wola', priceB=1000000))
getWebsite("https://www.google.com/")

"""
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
req = Request("http://www.111cn.net /")
try:
    response = urlopen(req)
except HTTPError as e:
    # do something
    print('Error code: ', e.code)
except URLError as e:
    # do something
    print('Reason: ', e.reason)
else:
    # do something
    print('good!')
"""
