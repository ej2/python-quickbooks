import base64
import requests
import json
from .exceptions import QuickbooksException

try:  # Python 3
    import http.client as httplib
    from urllib.parse import parse_qsl
except ImportError:  # Python 2
    import httplib
    from urlparse import parse_qsl

try:
    from rauth import OAuth1Session, OAuth1Service, OAuth2Session, OAuth2Service
except ImportError:
    print("Please import Rauth:\n\n")
    print("http://rauth.readthedocs.org/en/latest/\n")
    raise

SCOPE = (
    ('com.intuit.quickbooks.accounting', 'ACCOUNTING',),
    ('com.intuit.quickbooks.payment', 'PAYMENT',),
)


class AuthSessionManager(object):
    sandbox = False

    access_token = ''
    access_token_secret = ''
    consumer_key = ''
    consumer_secret = ''
    session = None
    started = False
    request_token = ''
    request_token_secret = ''

    def start_session(self):
        raise NotImplemented

    def get_session(self):
        if not self.started:
            self.start_session()

        return self.session


class Oauth1SessionManager(AuthSessionManager):
    request_token_url = "https://oauth.intuit.com/oauth/v1/get_request_token"
    access_token_url = "https://oauth.intuit.com/oauth/v1/get_access_token"
    authorize_url = "https://appcenter.intuit.com/Connect/Begin"
    current_user_url = "https://appcenter.intuit.com/api/v1/user/current"

    def __init__(self, **kwargs):
        if 'consumer_key' in kwargs:
            self.consumer_key = kwargs['consumer_key']

        if 'consumer_secret' in kwargs:
            self.consumer_secret = kwargs['consumer_secret']

        if 'access_token' in kwargs:
            self.access_token = kwargs['access_token']

        if 'access_token_secret' in kwargs:
            self.access_token_secret = kwargs['access_token_secret']

        if 'sandbox' in kwargs:
            self.sandbox = kwargs['sandbox']

    def start_session(self):
        if not self.started:
            if self.consumer_key == '':
                raise QuickbooksException("Consumer Key missing. Cannot create session.")

            if self.consumer_secret == '':
                raise QuickbooksException("Consumer Secret missing. Cannot create session.")

            if self.access_token == '':
                raise QuickbooksException("Access Token missing. Cannot create session.")

            if self.access_token_secret == '':
                raise QuickbooksException("Access Token Secret missing. Cannot create session.")

            self.session = OAuth1Session(
                self.consumer_key,
                self.consumer_secret,
                self.access_token,
                self.access_token_secret,
            )

            self.started = True

        return self.session

    def get_authorize_url(self, callback_url):
        """
        Returns the Authorize URL as returned by QB, and specified by OAuth 1.0a.
        :return URI:
        """
        self.authorize_url = self.authorize_url[:self.authorize_url.find('?')] \
            if '?' in self.authorize_url else self.authorize_url

        qb_service = OAuth1Service(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            request_token_url=self.request_token_url,
            access_token_url=self.access_token_url,
            authorize_url=self.authorize_url,
        )

        response = qb_service.get_raw_request_token(
            params={'oauth_callback': callback_url})

        oauth_resp = dict(parse_qsl(response.text))

        self.request_token = oauth_resp['oauth_token']
        self.request_token_secret = oauth_resp['oauth_token_secret']

        return qb_service.get_authorize_url(self.request_token)

    def get_access_tokens(self, oauth_verifier):
        """
        Wrapper around get_auth_session, returns session, and sets access_token and
        access_token_secret on the QB Object.
        :param oauth_verifier: the oauth_verifier as specified by OAuth 1.0a
        """
        session = self.qbService.get_auth_session(
            self.request_token,
            self.request_token_secret,
            data={'oauth_verifier': oauth_verifier})

        self.access_token = session.access_token
        self.access_token_secret = session.access_token_secret
        return session


class Oauth2SessionManager(AuthSessionManager):
    access_token_url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
    authorize_url = "https://appcenter.intuit.com/connect/oauth2"
    redirect_url = "http://localhost:8000"
    base_url = 'http://localhost:8000'

    client_id = ''
    client_secret = ''
    x_refresh_token_expires_in = 0
    access_token = ''
    token_type = ''
    refresh_token = ''
    expires_in = 0
    id_token = 0

    def __init__(self, **kwargs):
        if 'client_id' in kwargs:
            self.client_id = kwargs['client_id']

        if 'client_secret' in kwargs:
            self.client_secret = kwargs['client_secret']

        if 'access_token' in kwargs:
            self.access_token = kwargs['access_token']

        if 'base_url' in kwargs:
            self.base_url = kwargs['base_url']

        if 'sandbox' in kwargs:
            self.sandbox = kwargs['sandbox']

    def start_session(self):
        if not self.started:
            if self.consumer_key == '':
                raise QuickbooksException("Consumer Key missing. Cannot create session.")

            if self.consumer_secret == '':
                raise QuickbooksException("Consumer Secret missing. Cannot create session.")

            if self.access_token == '':
                raise QuickbooksException("Access Token missing. Cannot create session.")

            if self.access_token_secret == '':
                raise QuickbooksException("Access Token Secret missing. Cannot create session.")

            self.session = OAuth2Session(
                name='quickbooks',
                client_id=self.client_id,
                client_secret=self.client_secret,
                authorize_url=self.authorize_url,
                access_token_url=self.access_token_url,
                base_url=self.base_url,
            )

            self.started = True

        return self.session

    def get_authorize_url(self, callback_url):
        """
        Returns the Authorize URL as returned by QB, and specified by OAuth 1.0a.
        :return URI:
        """
        auth_service = OAuth2Service(
            name='quickbooks',
            client_id=self.client_id,
            client_secret=self.client_secret,
            authorize_url=self.authorize_url,
            access_token_url=self.access_token_url,
            base_url=self.base_url,
        )

        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'scope': 'com.intuit.quickbooks.accounting',
            'redirect_uri': callback_url,
            'state': 'quickbooksisdumb',
        }

        url = auth_service.get_authorize_url(**params)

        return url

    # def get_access_tokens_old(self, auth_code):
    #     """
    #     Wrapper around get_auth_session, returns session, and sets access_token and
    #     access_token_secret on the QB Object.
    #     :param oauth_verifier: the oauth_verifier as specified by OAuth 1.0a
    #     """
    #     auth_service = OAuth2Service(
    #         name='quickbooks',
    #         client_id=self.client_id,
    #         client_secret=self.client_secret,
    #         authorize_url=self.authorize_url,
    #         access_token_url=self.access_token_url,
    #         #base_url=self.base_url,
    #     )
    #
    #     data = {'code': auth_code,
    #             'grant_type': 'authorization_code',
    #             'redirect_uri': 'http://localhost:8000'}
    #
    #     session = auth_service.get_auth_session(data=data, decoder=json.loads)
    #     #session.access_token
    #
    #     return session

    def get_access_tokens(self, auth_code):
        auth_header = 'Basic ' + stringToBase64(self.client_id + ':' + self.client_secret)
        headers = {'Accept': 'application/json', 'content-type': 'application/x-www-form-urlencoded',
                   'Authorization': auth_header}
        payload = {
            'code': auth_code,
            'redirect_uri': self.base_url,
            'grant_type': 'authorization_code'
        }
        r = requests.post(self.access_token_url, data=payload, headers=headers)
        if r.status_code != 200:
            return r.text
        bearer_raw = json.loads(r.text)

        if 'id_token' in bearer_raw:
            idToken = idToken = bearer_raw['id_token']
        else:
            idToken = None

        self.x_refresh_token_expires_in = bearer_raw['x_refresh_token_expires_in']
        self.access_token = bearer_raw['access_token']
        self.token_type = bearer_raw['token_type']
        self.refresh_token = bearer_raw['refresh_token']
        self.expires_in = bearer_raw['expires_in']
        self.id_token = idToken

        # return Bearer(bearer_raw['x_refresh_token_expires_in'], bearer_raw['access_token'], bearer_raw['token_type'],
        #               bearer_raw['refresh_token'], bearer_raw['expires_in'], idToken=idToken)


def stringToBase64(s):
    return base64.b64encode(bytearray(s, 'utf-8')).decode()
    # return base64.b64encode(bytes(s, 'utf-8')).decode() # Python 3
