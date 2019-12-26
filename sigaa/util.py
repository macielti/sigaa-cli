import requests
import re


def generate_session(domain):
    """
    A function that recieve a domain string and return a **requests.Session()** object with cookies setted.

    :param domain: The platform domain of the university server. Need to be the same as the domain inputed in the class instatiation.
    :type domain: String

    :return: An unauthenticated session.
    :rtype: **requests.session.Session()**

    :raises NotValidDomain: An error occurred when a not valid sigaa platform domain is suplied as positional parameter.

    >>> from sigaa.api import API
    >>> session = API.generate_session("sigaa.ufpi.com")
    """

    session = requests.Session()
    r = session.get("https://%s/sigaa/verTelaLogin.do" %
                    domain, allow_redirects=True, stream=True)

    # verify if the domain really apoint to a valid SIGAA platform.
    if 'SIGAA' not in r.text:
        raise NotValidDomain("Not valid sigaa platform domain.")

    return session


def get_j_id_and_jsp(html_page):
    """
    This function recieve a html source code of a response and set the **j_id** and **j_id_jsp** parameters
    that is required to do some actions inside the platform. 

    You are not expected to use this method but if you need, there is...

    :param html_page: HTML response text.
    :type domain: String
    """

    # return the first ocurrence of the 'j_id'
    j_id = list(re.findall(r"j_id\d{1,4}", html_page))[0]
    j_id_jsp = list(re.findall(r"j_id_jsp_\d{4,}_\d+", html_page))[3]

    return (j_id, j_id_jsp)


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
