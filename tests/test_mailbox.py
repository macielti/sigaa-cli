import unittest
import requests
import re

import os
import sys
path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(path)

import sigaa
from sigaa.api import API
from sigaa.api import MailBox
from creds import login

class TestAPI(unittest.TestCase):
    
    def test_goto_mainbox_portal(self):
        api = API()
        api.authenticate(login['username'], login['passwd'])
        mail_box = MailBox(api.get_session(), api.get_domain())
        result = mail_box.goto_mainbox_portal()
        self.assertTrue(result)
    
    def test_goto_send_message(self):
        api = API()
        api.authenticate(login['username'], login['passwd'])
        mail_box = MailBox(api.get_session(), api.get_domain())
        mail_box.goto_mainbox_portal()
        result = mail_box.goto_send_message()
        self.assertTrue(result)
    
    def test_search(self):
        api = API()
        api.authenticate(login['username'], login['passwd'])
        mail_box = MailBox(api.get_session(), api.get_domain())
        mail_box.goto_mainbox_portal()
        mail_box.goto_send_message()
        result = mail_box.search('macielti')
        self.assertIn('BRUNO DO NASCIMENTO MACIEL (macielti)', result)


if __name__ == '__main__':
    unittest.main()