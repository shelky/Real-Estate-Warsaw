import csv

class apartment:
    """
    Basic class for apartments. Properties include:
    - int price
    - int area
    - str loc

    + for a review of the apartment use see method
    + for an export use method export

    """
    def __init__(self, price, area, loc = "NaN"):
        self.price = price
        self.area = area
        self.loc = loc

    def see(self):
        print("Price:", self.price)
        print("Area:", self.area)
        print("Localisation:", self.loc)


class apartmentAd:
    """
    Basic class for apartments. Properties include:
    - int price
    - int area
    - str loc

    + for a review of the apartment use see method
    + for an export use method export

    """
    def __init__(self, price, title, URL, timestamp):
        self.price = price
        self.URL = URL
        self.title = title
        self.timestamp = timestamp


    def see(self):
        print('-----------------------')
        print("Price:", self.price)
        print('Title:', self.title)
        print('URL:', self.URL)
        print('Timestamp:', self.timestamp)
        print('-----------------------')

def new_apartment(ap, file_name, pricesimilarity = 0.03):
    """
    Compares the particular apartment ad with the ads in the database and checks if it is a new entry. The comparison
    is based on the ad title and the price. There is a possibility to count as an old apartment even if the price
    changes slightly.
    :param ap: apartmentAd, the ad which we would like to compare with the entries from databse
    :param file_name: str, path to the csv database
    :param pricesimilarity: float, the relative fraction of how an ap price can differ from the entries in database
    to be still counted as an old ad.
    :return: bool, 1 if we have a new apartment ad, 0 if not
    """
    with open(file_name, newline='') as csvfile:
        apartmentreader = csv.reader(csvfile)
        for row in apartmentreader:
            if((ap.title == row[0]) and abs(1.0*(ap.price - int(row[1]))/ap.price) < pricesimilarity):
                return 0
    return 1

def export_apartment(ap, file_name):
    """
    Write apartment ad to database.
    :param ap: apartmentAd, the ad we would like to add to the database
    :param file_name: tr, path to the csv database
    :return:
    """
    with open(file_name, 'a', newline='') as csvfile:
        apartmentwriter = csv.writer(csvfile)
        apartmentwriter.writerow([ap.title, ap.price, ap.URL, ap.timestamp, 1])
    return 0
