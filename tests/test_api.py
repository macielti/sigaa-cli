import unittest
import requests

import os
import sys
path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(path)

import sigaa
from sigaa.api import API

class TestAPI(unittest.TestCase):

    def test_authenticate(self):
        api = API("sigaa.ufpi.br")
        result = api.authenticate('foo', 'bar')
        self.assertFalse(result)
    
    def test_get_sesson_id(self):
        api = API("sigaa.ufpi.br")
        result = api.get_sesson_id()
        # key JSESSIONID
        self.assertIn('JSESSIONID', result.keys())
    
    def test_generate_session(self):
        result = API.generate_session("sigaa.ufpi.br")
        self.assertIsInstance(result, requests.sessions.Session)
        self.assertIn('JSESSIONID', result.cookies.keys())

        # test exceptions
        with self.assertRaises(sigaa.api.NotValidDomain):
            API.generate_session("google.com")

if __name__ == '__main__':
    unittest.main()