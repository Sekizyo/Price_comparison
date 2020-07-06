import os
import unittest
import requests
from module.pretty import *

strings = ""
intigers = 0
floats = 1.2
tuples = ()
lists = [] 
dicts = {}
lower_strings = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z']
high_strings = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'y', 'Z']
spec_strings = ['Ł', 'ł']

class BasicTests(unittest.TestCase):

    def test_format_price(self):
        price = format_price(" ,205040\nzł\todsdfysedf8s0df7gsd-f7gas87dga- \xa0")

        self.assertEqual(type(price), type(strings))

        list_price = list(price)
        black_list = ['', ',', '\n', '\t', '\xa0']
        for letter in list_price:
            for x in black_list:
                self.assertNotIn(x, letter)

            for y in lower_strings:
                self.assertNotIn(y, letter)

            for z in high_strings:
                self.assertNotIn(z, letter)

            for t in spec_strings:
                self.assertNotIn(t, letter)

    def test_sort(self):
        name = ['Gigabyte GeForce RTX 2080 Ti AORUS 11GB GDDR6', 'ASUS GeForce RTX 2080 Ti ROG STRIX OC 11GB GDDR6', 'x-kom G4M3R 600 i9-10900K64GB500+1TBW10XRTX2080Ti', 'Inno3D GeForce RTX 2080 Ti X3 GAMING OC 11GB GDDR6']
        price = ['10', '12', '11', '9']
        url = ['asd', 'fsd', 'gd', 'rwe']
        #------
        name0, price0, url0 = sort(name, price, url, "name_low")

        self.assertEqual(type(name0), type(lists))
        self.assertEqual(type(price0), type(lists))
        self.assertEqual(type(url0), type(lists))

        correct_name_low_name = ['ASUS GeForce RTX 2080 Ti ROG STRIX OC 11GB GDDR6', 'Inno3D GeForce RTX 2080 Ti X3 GAMING OC 11GB GDDR6', 'Gigabyte GeForce RTX 2080 Ti AORUS 11GB GDDR6', 'x-kom G4M3R 600 i9-10900K64GB500+1TBW10XRTX2080Ti']
        self.assertEqual(name0, correct_name_low_name)

        correct_name_low_price = ['12', '9', '10', '11']
        self.assertEqual(price0, correct_name_low_price)

        correct_name_low_link = ['fsd', 'rwe', 'asd', 'gd']
        self.assertEqual(url0, correct_name_low_link)


        #------
        name0, price0, url0 = sort(name, price, url, "name_high")

        self.assertEqual(type(name0), type(lists))
        self.assertEqual(type(price0), type(lists))
        self.assertEqual(type(url0), type(lists))

        correct_name_low_name = ['x-kom G4M3R 600 i9-10900K64GB500+1TBW10XRTX2080Ti', 'Gigabyte GeForce RTX 2080 Ti AORUS 11GB GDDR6', 'Inno3D GeForce RTX 2080 Ti X3 GAMING OC 11GB GDDR6', 'ASUS GeForce RTX 2080 Ti ROG STRIX OC 11GB GDDR6']
        self.assertEqual(name0, correct_name_low_name)

        correct_name_low_price = ['11', '10', '9', '12']
        self.assertEqual(price0, correct_name_low_price)

        correct_name_low_link = ['gd', 'asd', 'rwe', 'fsd']
        self.assertEqual(url0, correct_name_low_link)


        #------
        name0, price0, url0 = sort(name, price, url, "price_low")

        self.assertEqual(type(name0), type(tuples))
        self.assertEqual(type(price0), type(tuples))
        self.assertEqual(type(url0), type(tuples))

        correct_name_low_name = ('Inno3D GeForce RTX 2080 Ti X3 GAMING OC 11GB GDDR6', 'Gigabyte GeForce RTX 2080 Ti AORUS 11GB GDDR6', 'x-kom G4M3R 600 i9-10900K64GB500+1TBW10XRTX2080Ti', 'ASUS GeForce RTX 2080 Ti ROG STRIX OC 11GB GDDR6')
        self.assertEqual(name0, correct_name_low_name)

        correct_name_low_price = (9, 10, 11, 12)
        self.assertEqual(price0, correct_name_low_price)

        correct_name_low_link = ('rwe', 'asd', 'gd', 'fsd')
        self.assertEqual(url0, correct_name_low_link)

        #------
        name0, price0, url0 = sort(name, price, url, "price_high")

        self.assertEqual(type(name0), type(tuples))
        self.assertEqual(type(price0), type(tuples))
        self.assertEqual(type(url0), type(tuples))

        correct_name_low_name = ('ASUS GeForce RTX 2080 Ti ROG STRIX OC 11GB GDDR6', 'x-kom G4M3R 600 i9-10900K64GB500+1TBW10XRTX2080Ti', 'Gigabyte GeForce RTX 2080 Ti AORUS 11GB GDDR6', 'Inno3D GeForce RTX 2080 Ti X3 GAMING OC 11GB GDDR6')
        self.assertEqual(name0, correct_name_low_name)

        correct_name_low_price = (12, 11, 10, 9)
        self.assertEqual(price0, correct_name_low_price)

        correct_name_low_link = ('fsd', 'gd', 'asd', 'rwe')
        self.assertEqual(url0, correct_name_low_link)


        


            




if __name__ == "__main__":
    unittest.main()