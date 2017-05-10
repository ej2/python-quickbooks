try:  # Python 3
    from urllib.parse import parse_qs, urlparse
    from http.server import BaseHTTPRequestHandler, HTTPServer
except ImportError:  # Python 2
    from urlparse import parse_qs, urlparse
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

    def bytes(value, encoding):
        return str(value)

from quickbooks import QuickBooks


class QuickBooksAuthHandler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        qb_data = self.server.qb_data

        GET = parse_qs(urlparse(self.path).query)

        oauth_verifier = GET.get('oauth_verifier')
        realm_id = GET.get('realmId')

        if type(realm_id) is list and len(realm_id) == 1:
            realm_id = realm_id[0]

        if oauth_verifier and realm_id:
            client = self.server.qb_client_class(
                sandbox=qb_data['sandbox'],
                consumer_key=qb_data['consumer_key'],
                consumer_secret=qb_data['consumer_secret']
            )

            client.authorize_url = qb_data['authorize_url']
            client.request_token = qb_data['request_token']
            client.request_token_secret = qb_data['request_token_secret']
            client.set_up_service()

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


class QuickBooksAuthServer(HTTPServer):

    qb_client_class = QuickBooks

    @classmethod
    def build_server(cls, consumer_key, consumer_secret, sandbox, port):
        client = cls.qb_client_class(
            sandbox=sandbox,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            callback_url='http://localhost:{0}'.format(port)
        )

        qb_data = {
            'authorize_url': client.get_authorize_url(),
            'request_token': client.request_token,
            'request_token_secret': client.request_token_secret,
            'consumer_key': consumer_key,
            'consumer_secret': consumer_secret,
            'sandbox': sandbox,
        }

        instance = cls(('', port), QuickBooksAuthHandler)
        instance.qb_data = qb_data

        return instance
