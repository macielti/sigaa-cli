import requests
import re
from tqdm import tqdm
from .mailbox import MailBox
import sigaa.util as util



class API:
    """ 
    Class to instantiate the API object.

    :param domain: The platform domain of the university server.
    :type domain: String

    :attr session: Holds a :class:`requests.Session()` object.

    >>> from sigaa.api import API
    >>> api = API("sigaa.ufma.br") # already executes API.generate_session(domain)
    """

    def __init__(self, domain="sigaa.ufpi.br"):
        self.__domain = domain
        self.__session = util.generate_session(self.__domain)
        self.__j_id = None
        self.__j_id_jsp = None

    def authenticate(self, username, passwd):
        """
        Method to authenticate the :attr:`sigaacli.API.session`.

        :param username: The username of the student.
        :type username: String
        :param passwd: The password of the student.
        :type passwd: String

        :return: **True** for success or **False** for failure.
        :rtype: **Boolean**

        >>> from sigaa.api import API
        >>> api = API("sigaa.ufpi.br")
        >>> api.authenticate("username", "password")
        False or True
        """

        url = 'https://%s/sigaa/logar.do?dispatch=logOn' % self.__domain
        pyload = {
            'user.login': username,
            'user.senha': passwd
        }

        r = self.__session.post(url, data=pyload)

        if "rio e/ou senha inv" not in r.text:
            # extract j_id parameters
            (self.__j_id, self.__j_id_jsp) = util.get_j_id_and_jsp(r.text)
            return True

        return False

    def deauthenticate(self):
        """
        Method to execute the logOff operation on SIGAA platform. 
        It will return True is the operation was executed with success.

        :return: **True** if the session was deauthenticated with success or **False** if it fails.
        :rtype: Boolean

        >>> from sigaa.api import API
        >>> api = API('sigaa.ufma.br')
        >>> api.authenticate('macielti', 'PaSsWoRd')
        False
        >>> api.deauthenticate()
        True
        """
        # logOff operation from 'discente' portal.
        r = self.__session.get("https://%s/sigaa/logar.do?dispatch=logOff" %
                               self.__domain, allow_redirects=True)
        return not self.is_authenticated()

    def get_session(self):
        """
        Method that returns a requests.Session() object.
        """
        return self.__session

    def get_domain(self):
        """
        Method that returns the setted domain.
        """
        return self.__domain

    def is_authenticated(self):
        """
        Method that returns the if the session is authenticated or not.

        :return: True if you are authenticated or False if not.
        :rtype: Boolean

        >>> from sigaa.api import API
        >>> api = API('sigaa.ufma.br')
        >>> api.is_authenticated()
        False
        """
        r = self.__session.get("https://%s/sigaa/verPortalDiscente.do" %
                               self.__domain, allow_redirects=True)
        if "o foi expirada. " not in r.text:
            # extract j_id parameters
            (self.__j_id, self.__j_id_jsp) = util.get_j_id_and_jsp(r.text)
            return True
        return False
        
    def get_all_users(self):
        """
        Method to scrap the fullname and username of all the users of the platform.

        :return: List of users infos. 
        :rtype: list. Example: ['BRUNO DO NASCIMENTO MACIEL (macielti)', ...]
        """

        chars = [
            'a',
            'b',
            'c',
            'd',
            'e',
            'f',
            'g',
            'h',
            'i',
            'j',
            'k',
            'l',
            'm',
            'n',
            'o',
            'p',
            'q',
            'r',
            's',
            't',
            'u',
            'v',
            'w',
            'x',
            'y',
            'z',

            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '0',

        ]

        mail_box = MailBox(self.__session, self.__domain)
        mail_box.goto_mainbox_portal()
        mail_box.goto_send_message()
        
        users = []
        for char in tqdm(chars):
            users = users + mail_box.search(char)
        
        return sorted(set(users))
