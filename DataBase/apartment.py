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

a1 = apartment(550000,54, 'ochota')
print(a1.loc)
print(a1.price)
a1.see()