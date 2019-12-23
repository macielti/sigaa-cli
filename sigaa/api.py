import requests

class API:
    """ 
    Class to instantiate the API object.

    :param domain: The platform domain of the university server.
    :type domain: String

    :attr session: Holds a :class:`requests.Session()` object.
    """
    def __init__(self, domain="sigaa.ufpi.br"):
        self._domain = domain
        self.__session = API.generate_session(self._domain)

    def authenticate(self, username, passwd):
        """
        Method to authenticate the :attr:`sigaacli.API.session`.

        :param username: The username of the student.
        :type username: String
        :param passwd: The password of the student.
        :type passwd: String

        :return: **True** for success or **False** for failure.
        :rtype: **Boolean**
        """

        url = 'https://%s/sigaa/logar.do?dispatch=logOn' % self._domain
        pyload = {
            'user.login':username,
            'user.senha':passwd
        }

        r = self.__session.post(url, data=pyload, stream=True)
        
        if "rio e/ou senha inv" not in r.text:
            return True
            
        return False
    
    def get_sesson_id(self):
        """
        Method that returns a dictionary with the JSESSIONID and cookies.

        :return: A cookie dictionary.
        :rtype: dict
        """
        return self.__session.cookies.get_dict()


    @staticmethod
    def generate_session(domain):
        """
        A static method that recieve a domain string and return a **requests.Session()** object with cookies setted.

        :param domain: The platform domain of the university server. Need to be the same as the domain inputed in the class instatiation.
        :type domain: String

        :return: An unauthenticated session.
        :rtype: **requests.Session()**

        :raises NotValidDomain: An error occurred when a not valid sigaa platform domain is suplied as positional parameter.
        """
        
        session = requests.Session()
        r = session.get("https://%s/sigaa/verTelaLogin.do" % domain, allow_redirects=True, stream=True)

        # verify if the domain really apoint to a valid SIGAA platform.
        if 'SIGAA' not in r.text:
            raise NotValidDomain("Not valid sigaa platform domain.")

        return session

class NotValidDomain(Exception):
    """
    Is raised when a not valid sigaa platform domain is suplied 
    as parameter to the sigaa.API.generate_session() static method.
    """
    def __init___(self, message):
        super(NotValidDomain, self).__init__(message)