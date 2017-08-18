from quickbooks.auth import Oauth1SessionManager, Oauth2SessionManager

try:  # Python 3
    from urllib.parse import parse_qs, urlparse
    from http.server import BaseHTTPRequestHandler, HTTPServer
except ImportError:  # Python 2
    from urlparse import parse_qs, urlparse
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

    def bytes(value, encoding):
        return str(value)


class QuickBooksAuthHandler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

    def do_GET(self):
        qb_data = self.server.qb_data
        oauth_version = qb_data['oauth_version']

        if oauth_version == 1:
            self.get_oauth_1()
        elif oauth_version == 2:
            self.get_oauth_2()

    def get_oauth_1(self):
        self._set_headers()
        qb_data = self.server.qb_data

        GET = parse_qs(urlparse(self.path).query)

        oauth_verifier = GET.get('oauth_verifier')
        realm_id = GET.get('realmId')

        if type(realm_id) is list and len(realm_id) == 1:
            realm_id = realm_id[0]

        if oauth_verifier and realm_id:
            client = Oauth1SessionManager(
                sandbox=qb_data['sandbox'],
                consumer_key=qb_data['consumer_key'],
                consumer_secret=qb_data['consumer_secret']
            )

            client.authorize_url = qb_data['authorize_url']
            client.request_token = qb_data['request_token']
            client.request_token_secret = qb_data['request_token_secret']
            client.get_access_tokens(oauth_verifier)

            self.wfile.write(
                bytes('<h1>QuickBooks auth handled with success!</h1>',
                      'UTF-8'))
            self.wfile.write(
                bytes('<p><b>Sandbox:</b> {0}</p>'.format(qb_data['sandbox']),
                      'UTF-8'))
            self.wfile.write(
                bytes('<p><b>Realm Id:</b> {0}</p>'.format(realm_id), 'UTF-8'))

            self.wfile.write(
                bytes('<p><b>Access Token:</b> {0}</p>'.format(
                    client.access_token), 'UTF-8'))
            self.wfile.write(
                bytes('<p><b>Access Token Secret:</b> {0}</p>'.format(
                    client.access_token_secret), 'UTF-8'))
        else:
            self.wfile.write(
                bytes('<h1>QuickBooks auth failed, try again.</h1>', 'UTF-8'))

    def get_oauth_2(self):
        self._set_headers()
        qb_data = self.server.qb_data

        GET = parse_qs(urlparse(self.path).query)
        auth_code = GET.get('code')

        if auth_code:
            client = Oauth2SessionManager(
                sandbox=qb_data['sandbox'],
                client_id=qb_data['consumer_key'],
                client_secret=qb_data['consumer_secret'],
                callback_url=qb_data['callback_url'],
                base_url=qb_data['base_url'],
            )

            client.get_access_tokens(auth_code)

            self.wfile.write(
                bytes('<h1>QuickBooks auth handled with success!</h1>',
                      'UTF-8'))
            self.wfile.write(
                bytes('<p><b>Sandbox:</b> {0}</p>'.format(qb_data['sandbox']),
                      'UTF-8'))
            self.wfile.write(
                bytes('<p><b>Access Token:</b> {0}</p>'.format(
                    client.access_token), 'UTF-8'))
            self.wfile.write(
                bytes('<p><b>Refresh Token:</b> {0}</p>'.format(
                    client.refresh_token), 'UTF-8'))
            self.wfile.write(
                bytes('<p><b>Expires In:</b> {0}</p>'.format(
                    client.expires_in), 'UTF-8'))
        else:
            self.wfile.write(
                bytes('<h1>QuickBooks auth failed, try again.</h1>', 'UTF-8'))


class QuickBooksAuthServer(HTTPServer):
    @classmethod
    def build_server(cls, consumer_key, consumer_secret, sandbox, port, oauth_version):
        callback_url = 'http://localhost:{0}'.format(port)
        if oauth_version == 1:
            client = Oauth1SessionManager(
                sandbox=sandbox,
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
            )

            qb_data = {
                'authorize_url': client.get_authorize_url(callback_url),
                'request_token': client.request_token,
                'request_token_secret': client.request_token_secret,
                'consumer_key': consumer_key,
                'consumer_secret': consumer_secret,
                'sandbox': sandbox,
                'oauth_version': oauth_version,
            }

        elif oauth_version == 2:
            client = Oauth2SessionManager(
                sandbox=sandbox,
                client_id=consumer_key,
                client_secret=consumer_secret,
                base_url='http://localhost:{0}'.format(port),
            )

            qb_data = {
                'authorize_url': client.get_authorize_url(callback_url),
                'access_token': client.access_token,
                'refresh_token': client.refresh_token,
                'consumer_key': consumer_key,
                'consumer_secret': consumer_secret,
                'token_type': client.token_type,
                'expires_in': client.expires_in,
                'x_refresh_token_expires_in': client.x_refresh_token_expires_in,
                'sandbox': sandbox,
                'oauth_version': oauth_version,
                'callback_url': 'http://localhost:{0}'.format(port),
                'base_url': 'http://localhost:{0}'.format(port),
            }

        else:
            raise Exception('Invalid OAuth version number. Version number must be 1 or 2.')

        instance = cls(('', port), QuickBooksAuthHandler)
        instance.qb_data = qb_data

        return instance
