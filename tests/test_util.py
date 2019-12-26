import unittest
import requests
import re

import os
import sys
path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(path)

import sigaa.util as util


class TestUtil(unittest.TestCase):

    def test_generate_session(self):
        # ufpi
        result = util.generate_session("sigaa.ufpi.br")
        self.assertIsInstance(result, requests.sessions.Session)
        self.assertIn('JSESSIONID', result.cookies.keys())

        # test exceptions
        with self.assertRaises(util.NotValidDomain):
            util.generate_session("google.com")

if __name__ == '__main__':
    unittest.main()