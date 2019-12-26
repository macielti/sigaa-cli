import unittest
import requests
import re

import os
import sys
path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(path)
from sigaa.api import API
import sigaa

class TestAPI(unittest.TestCase):

    def test_authenticate(self):
        # ufpi
        api = API("sigaa.ufpi.br")
        result = api.authenticate('foo', 'bar')
        self.assertFalse(result)

    def test_deauthenticate(self):
        # ufpi
        api = API("sigaa.ufpi.br")
        api.authenticate('foo', 'bar')
        result = api.deauthenticate()
        self.assertTrue(result)

    def test_get_session(self):
        # ufpi
        api = API("sigaa.ufpi.br")
        result = api.get_session()
        self.assertIsInstance(result, requests.Session)

    def test_is_authenticated(self):
        # ufpi
        api = API("sigaa.ufpi.br")
        result = api.is_authenticated()
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
