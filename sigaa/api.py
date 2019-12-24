import requests
import re

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
        self._domain = domain
        self.__session = API.generate_session(self._domain)
        self.__j_id = None

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

        url = 'https://%s/sigaa/logar.do?dispatch=logOn' % self._domain
        pyload = {
            'user.login':username,
            'user.senha':passwd
        }

        r = self.__session.post(url, data=pyload, stream=True)
        
        if "rio e/ou senha inv" not in r.text:
            self.__auth = True
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
        r = self.__session.get("https://%s/sigaa/logar.do?dispatch=logOff" % self._domain, allow_redirects=True, stream=True)
        return not self.is_authenticated()
    
    def get_sesson_id(self):
        """
        Method that returns a dictionary with the JSESSIONID and cookies.

        :return: A cookie dictionary.
        :rtype: dict

        >>> from sigaa.api import API
        >>> api = API("sigaa.ufpi.br")
        >>> api.get_session_id()
        {'JSESSIONID': '86A4C148844BCD2684011B45348D6294.jb06'}
        """
        return self.__session.cookies.get_dict()
    
    def is_authenticated(self):
        """
        Method that returns the if the session is authenticated or not.
        
        :return: True if you are authenticated or False if not.
        :rtype: Boolean

        :todo: More sofisticated verification via request.

        >>> from sigaa.api import API
        >>> api = API('sigaa.ufma.br')
        >>> api.is_authenticated()
        False
        """
        r = self.__session.get("https://%s/sigaa/verPortalDiscente.do" % self._domain, allow_redirects=True, stream=True)
        if "o foi expirada. " not in r.text:
            return True
        return False


    @staticmethod
    def generate_session(domain):
        """
        A static method that recieve a domain string and return a **requests.Session()** object with cookies setted.

        :param domain: The platform domain of the university server. Need to be the same as the domain inputed in the class instatiation.
        :type domain: String

        :return: An unauthenticated session.
        :rtype: **requests.session.Session()**

        :raises NotValidDomain: An error occurred when a not valid sigaa platform domain is suplied as positional parameter.

        >>> from sigaa.api import API
        >>> session = API.generate_session("sigaa.ufpi.com")
        """
        
        session = requests.Session()
        r = session.get("https://%s/sigaa/verTelaLogin.do" % domain, allow_redirects=True, stream=True)

        # verify if the domain really apoint to a valid SIGAA platform.
        if 'SIGAA' not in r.text:
            raise NotValidDomain("Not valid sigaa platform domain.")

        return session

    @staticmethod
    def get_j_id(html_page):
        """
        This static method recieve a html source code of a response and return the **j_id** parameter
        that is required to do some actions inside the platform. 
        
        You are not expected to use this method but if you need, there is...

        :param html_page: HTML response text.
        :type domain: String

        :return: The j_id parameter like 'j_id3'
        :rtype: String
        """
        # return the first ocurrence of the 'j_id'
        return re.findall(r"j_id+\d{1,4}", html_page)[0] 

class NotValidDomain(Exception):
    """
    Is raised when a not valid sigaa platform domain is suplied 
    as parameter to the sigaa.API.generate_session() static method.

    >>> from sigaa.api import API
    >>> API.generate_session("google.com")
    Traceback (most recent call last):
     ...
    sigaa.api.NotValidDomain: Not valid sigaa platform domain.
    """
    def __init___(self, message):
        super(NotValidDomain, self).__init__(message)