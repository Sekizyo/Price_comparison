import os
import unittest
import requests
from module.check import *
class BasicTests(unittest.TestCase):
    def test_x_kom(self):
        name, prices, urls = x_kom("2080ti")

        strings = ""
        intiger = 0

        self.assertEqual(len(name), len(prices))
        self.assertEqual(len(name), len(urls))

        for word in name:
            self.assertEqual(type(word), type(strings))

        for price in prices:
            self.assertEqual(type(price), type(intiger))

        for x in range(1):
            response = requests.get(urls[x])
            self.assertEqual(response.ok, True)

        










if __name__ == "__main__":
    unittest.main()