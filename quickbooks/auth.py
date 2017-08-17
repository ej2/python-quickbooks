try:  # Python 3
    import http.client as httplib
    from urllib.parse import parse_qsl
except ImportError:  # Python 2
    import httplib
    from urlparse import parse_qsl

from .exceptions import QuickbooksException

try:
    from rauth import OAuth1Session, OAuth1Service, OAuth2Session
except ImportError:
    print("Please import Rauth:\n\n")
    print("http://rauth.readthedocs.org/en/latest/\n")
    raise


SCOPE = (
    ('com.intuit.quickbooks.accounting', 'ACCOUNTING',),
    ('com.intuit.quickbooks.payment', 'PAYMENT',),
)

request_oauth_2 = "https://appcenter.intuit.com/connect/oauth2"

# GET https://appcenter.intuit.com/connect/oauth2?
#  client_id=Q3ylJatCvnkYqVKLmkH1zWlNzNWB5CkYB36b5mws7HkKUEv9aI&
#  response_type=code&
#  scope=com.intuit.quickbooks.accounting&
#  redirect_uri=https://www.mydemoapp.com/oauth-redirect&
#  state=security_token%3D138r5719ru3e1%26url%3Dhttps://www.mydemoapp.com/oauth-redirect&


class AuthSessionManager(object):
    access_token = ''
    access_token_secret = ''
    consumer_key = ''
    consumer_secret = ''
    callback_url = ''
    sandbox = False
    session = None
    started = False
    request_token = ''
    request_token_secret = ''

    def __new__(cls, **kwargs):
        instance = object.__new__(cls)

        if 'consumer_key' in kwargs:
            instance.consumer_key = kwargs['consumer_key']

        if 'consumer_secret' in kwargs:
            instance.consumer_secret = kwargs['consumer_secret']

        if 'access_token' in kwargs:
            instance.access_token = kwargs['access_token']

        if 'access_token_secret' in kwargs:
            instance.access_token_secret = kwargs['access_token_secret']

        if 'callback_url' in kwargs:
            instance.callback_url = kwargs['callback_url']

        if 'sandbox' in kwargs:
            instance.sandbox = kwargs['sandbox']

        return instance

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

    def get_authorize_url(self):
        """
        Returns the Authorize URL as returned by QB, and specified by OAuth 1.0a.
        :return URI:
        """
        self.authorize_url = self.authorize_url[:self.authorize_url.find('?')] \
            if '?' in self.authorize_url else self.authorize_url

        qb_service = OAuth1Service(
            name=None,
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            request_token_url=self.request_token_url,
            access_token_url=self.access_token_url,
            authorize_url=self.authorize_url,
            base_url=None
        )

        response = qb_service.get_raw_request_token(
            params={'oauth_callback': self.callback_url})

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


class Oauth2Session(AuthSessionManager):
    request_token_url = "https://oauth.intuit.com/oauth/v1/get_request_token"
    access_token_url = "https://oauth.intuit.com/oauth/v1/get_access_token"
    authorize_url = "https://appcenter.intuit.com/connect/oauth2"
    current_user_url = "https://appcenter.intuit.com/api/v1/user/current"

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
                self.consumer_key,
                self.consumer_secret,
                self.access_token,
                self.access_token_secret,
            )

            self.started = True

        return self.session
