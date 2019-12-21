# encoding: utf-8
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

        Example of usage:

        >>> api = API("sigaa.ufpi.br")
        >>> api.authenticate('foo', 'bar')
        False
        """

        url = 'https://%s/sigaa/logar.do?dispatch=logOn' % self.domain
        pyload = {
            'user.login':username,
            'user.senha':passwd
        }

        r = self.__session.post(url, data=pyload, stream=True)
        
        if "Usuário e/ou senha inválidos" not in r.text:
            return True
            
        return False

    @staticmethod
    def generate_session(domain):
        """
        A static method that recieve a domain string and return a **requests.Session()** object with cookies setted.

        :param domain: The platform domain of the university server. Need to be the same as the domain inputed in the class instatiation.
        :type domain: String

        :return: An unauthenticated session.
        :rtype: **requests.Session()**

        Examples of usage:

        >>> session = API.generate_session("sigaa.ufpi.br")
        >>> session.cookies.keys()
        ['JSESSIONID']

        SIGAA Mobile:

        >>> session = API.generate_session("sig.ufob.edu.br")
        >>> session.cookies.keys()
        ['JSESSIONID']

        :todo: Verify if the domain points to a really valid SIGAA platform.
        """
        
        session = requests.Session()
        session.get("https://%s/sigaa/verTelaLogin.do" % domain, allow_redirects=True, stream=True)
        return session
    