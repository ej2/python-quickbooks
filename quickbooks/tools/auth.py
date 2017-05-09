import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from quickbooks import QuickBooks


class QuickBooksAuthHandler(BaseHTTPRequestHandler):

    consumer_key = ''
    consumer_secret = ''
    authorize_url = ''
    request_token = ''
    request_token_secret = ''
    sandbox = False

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

        GET = urlparse.parse_qs(urlparse.urlparse(self.path).query)

        oauth_verifier = GET.get('oauth_verifier')
        realm_id = GET.get('realmId')
        if oauth_verifier and realm_id:
            client = QuickBooks(
                sandbox=self.sandbox,
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret
            )

            client.authorize_url = self.authorize_url
            client.request_token = self.request_token
            client.request_token_secret = self.request_token_secret
            client.set_up_service()

            client.get_access_tokens(oauth_verifier)

            self.wfile.write("<h1>QuickBooks auth handled with success!</h1>")
            self.wfile.write('<p><b>Sandbox:</b> {}</p>'.format(self.sandbox))
            self.wfile.write('<p><b>Realm Id:</b> {}</p>'.format(realm_id[0]))
            self.wfile.write('<p><b>Access Token:</b> {}</p>'.format(
                client.access_token))
            self.wfile.write('<p><b>Access Token Secret:</b> {}</p>'.format(
                client.access_token_secret))
        else:
            self.wfile.write("<h1>QuickBooks auth failed, try again.</h1>")


def handle_auth(consumer_key, consumer_secret, sandbox=False, port=8080):
    client = QuickBooks(
        sandbox=sandbox,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        callback_url='http://localhost:{}'.format(port)
    )

    # ugly hack, needs fixing
    QuickBooksAuthHandler.authorize_url = client.get_authorize_url()
    QuickBooksAuthHandler.request_token = client.request_token
    QuickBooksAuthHandler.request_token_secret = client.request_token_secret
    QuickBooksAuthHandler.consumer_key = consumer_key
    QuickBooksAuthHandler.consumer_secret = consumer_secret
    QuickBooksAuthHandler.sandbox = sandbox

    print 'Authorization url (ctrl+click to access):\n{}'.format(
        QuickBooksAuthHandler.authorize_url)

    server = HTTPServer(('', port), QuickBooksAuthHandler)
    server.serve_forever()
