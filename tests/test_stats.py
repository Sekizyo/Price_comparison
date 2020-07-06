import os
import unittest
from module.stats import return_query_stats
from module import app, db

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
    # query_base = 
    def setUp():
        now_date = "1-9-1939"
        now_time = "12:12:12"
        run_time = "40.1731252670288"
        added = "603"
        total = "603"

        query = Query(date=now_date, time=now_time, run_time=time, added=added, total=total)
        print('-----------', 'type(query)', type(query)) 
        
        query_base = query
        db.session.add(query)
        db.session.commit()

    def tearDown():

        db.session.delete(query)
        db.session.commit()


if __name__ == "__main__":
    unittest.main()