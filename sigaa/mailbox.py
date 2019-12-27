import re
import requests
import sigaa.util as util


class MailBox:
    """
    Class to viabilizate some operations on Mail Box of the SIGAA Portal.
    Created to be used mainly by the **sigaa.api.API**, use only if you know what you are doing.

    :param session: An autheticated requests.Session from sigaa.api.API.
    :type session: requests.Session
    :param domain: The domain of the SIGAA platform of the university server. Example: 'sigaa.ufpi.br'
    :type domain: String
    """

    def __init__(self, session, domain):
        self.__session = session
        self.__domain = domain
        self.__j_id = None
        self.__j_id_jsp = None

    def goto_mainbox_portal(self):
        """
        Request the Mailbox portal.

        :return: **True** for success or **False** for failure.
        :rtype: **Boolean**

        >>> from sigaa.api import API
        >>> from sigaa.mailbox import MailBox
        >>> api = API()
        >>> api.authenticate('macielti', '9pfP52ZpB5eE')
        >>> mail_box = MailBox(api.get_session(), api.get_domain())
        >>> mail_box.goto_mainbox_portal()
        """
        url = "https://www.%s/sigaa/abrirCaixaPostal.jsf?sistema=2" % self.__domain
        r = self.__session.get(url, allow_redirects=True,)

        # extract domain from response url
        self.__domain = re.findall(
            r"^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)", r.url)[0]

        # verify the success of the operation
        if "Registro(s) Encontrado(s)" in r.text:
            (self.__j_id, self.__j_id_jsp) = util.get_j_id_and_jsp(r.text)
            return True
        return False
        
    def goto_send_message(self):
        """
        This method acess the page used to send messages.

        :return: **True** for success or **False** for failure.
        :rtype: **Boolean**

        >>> from sigaa.api import API
        >>> from sigaa.mailbox import MailBox
        >>> api = API()
        >>> api.authenticate('macielti', '9pfP52ZpB5eE')
        >>> mail_box = MailBox(api.get_session(), api.get_domain())
        >>> mail_box.goto_mainbox_portal()
        >>> mail_box.goto_send_message()
        True
        """

        url = "https://www.%s/cxpostal/caixa_postal.jsf" % self.__domain
        payload = {
            'form': 'form',
            'form:selectOpMarcarMsg': '8',
            'form:SelectOneMenuPaginacao': '0',
            'javax.faces.ViewState': self.__j_id,
            'form:cmdMsg': 'form:cmdMsg'
        }
        r = self.__session.post(url, data=payload, allow_redirects=True)

        # verify the success of the operation
        if "<caption>Anexar Arquivos</caption>" in r.text:
            (self.__j_id, self.__j_id_jsp) = util.get_j_id_and_jsp(r.text)
            return True
        return False


    def search(self, query, subject="", message=""):
        """
        Search the users using the AJAX requisition.

        :param query: Search users by partial or full match on username. Example: "macielti"
        :type query: String
        :param subject: Subject of the message **(optional)**.
        :type subject: String
        :param message: Message text **(optional)**.
        :type message: String

        :return: List of users info provided by the platform.
        :rtype: list

        >>> from sigaa.api import API
        >>> from sigaa.mailbox import MailBox
        >>> api = API()
        >>> api.authenticate('macielti', '9pfP52ZpB5eE')
        >>> mail_box = MailBox(api.get_session(), api.get_domain())
        >>> mail_box.goto_mainbox_portal()
        >>> mail_box.goto_send_message()
        >>> mail_box.search('macielti')
        ['BRUNO DO NASCIMENTO MACIEL (macielti)']
        """

        url = "https://www.%s/cxpostal/envia_mensagem.jsf" % self.__domain

        payload = {
            'AJAXREQUEST': self.__j_id_jsp,
            'form': 'form',
            'form:usuarioAuto': query,
            'form:suggestion_selection': '',
            'form:assunto': subject,
            'form:texto': message,
            'form:nome': '',
            'form:arquivo2': '',
            'javax.faces.ViewState': self.__j_id,
            'form:suggestion': 'form:suggestion',
            'ajaxSingle': 'form:suggestion',
            'inputvalue': query,
            'AJAX:EVENTS_COUNT': '1'
        }
        r = self.__session.post(url, data=payload, allow_redirects=True)

        users = re.findall(r"(?:\w+\s)+\(.+?\)", r.text)

        return sorted(set(users))
    
    def simulate_user_selection(self, user, subject="", message=""):
        """
        Simulate the select operation. It's required when adding an user as recipient
        of a message. Created to be used inside the `MailBox.add_user_recipient()` method.

        :param user: User to simulate seletion. Example: "BRUNO DO NASCIMENTO MACIEL (macielti)"
        :type user: String
        :param subject: Subject of the message **(optional)**.
        :type subject: String
        :param message: Message text **(optional)**.
        :type message: String
       
        :return: **True** for success or **False** for failure.
        :rtype: **Boolean**
        """
        url = "https://www.%s/cxpostal/envia_mensagem.jsf" % self.__domain
        payload = {
            'AJAXREQUEST' : self.__j_id_jsp,
            'form' : 'form',
            'form:usuarioAuto' : user, #user complete  data string
            'form:suggestion_selection' : '0',
            'form:assunto' : subject,
            'form:texto' : message,
            'form:nome'	: '',
            'form:arquivo2'	: '',
            'form:confLeitura' : 'on',
            'form:enviarEmail' : 'on',
            'javax.faces.ViewState' : self.__j_id,
            'form:suggestion:%s12' % self.__j_id_jsp[:-1] : 'form:suggestion:%s12' % self.__j_id_jsp[:-1]
        }

        r = self.__session.post(url, data=payload)

        if "Ajax-Update-Ids" in r.text:
            return True
        return False

    def add_user_recipient(self, user, subject="", message=""):
        """
        Add user as recipient of the message

        :param user: User to be added as recipient of the message. Example: "BRUNO DO NASCIMENTO MACIEL (macielti)"
        :type user: String
        :param subject: Subject of the message **(optional)**.
        :type subject: String
        :param message: Message text **(optional)**.
        :type message: String

        :return: **True** for success or **False** for failure.
        :rtype: **Boolean**
        """
        url = "https://www.%s/cxpostal/envia_mensagem.jsf" % self.__domain
        payload = {
            'AJAXREQUEST' : self.__j_id_jsp,
            'form' : 'form',
            'form:usuarioAuto' : user,
            'form:suggestion_selection' : '',
            'form:assunto' : subject,
            'form:texto' : message,
            'form:nome' : '',
            'form:arquivo2' : '',
            'form:confLeitura' : 'on',
            'form:enviarEmail' : 'on',
            'javax.faces.ViewState' : self.__j_id,
            'form:addDestinatario' : 'form:addDestinatario'
        }

        self.search(user.split(' ')[-1].strip('(').strip(')')) # only the username part
        self.simulate_user_selection(user)

        r = self.__session.post(url, data=payload)

        if user.split(' ')[-1].strip('(').strip(')') in r.text:
            return True
        return False
    
    def send_message(self, subject, message):
        """
        Send message to previusly added users.
        
        Created to be used mainly by the **sigaa.api.API**, use only if you know what you are doing.

        :param subject: Subject of the message.
        :type subject: String
        :param message: Message text.
        :type message: String

        :return: **True** for success or **False** for failure.
        :rtype: **Boolean**
        """
        url = "https://www.%s/cxpostal/envia_mensagem.jsf" % self.__domain
        payload = {
            'form' : 'form',
            'form:usuarioAuto' : '',
            'form:suggestion_selection' : '',
            'form:assunto' : subject,
            'form:texto' : message,
            'form:nome' : '',
            'form:arquivo2' : '',
            'form:confLeitura' : 'on',
            'form:enviarEmail' : 'on',
            'form:btnBotaoCancelar' : 'Enviar',
            'javax.faces.ViewState' : self.__j_id,
        }

        r = self.__session.post(url, data=payload)

        if 'Mensagem enviada com sucesso' in r.text:
            return True
        return False