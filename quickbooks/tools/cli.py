import argparse

from quickbooks.tools.auth import QuickBooksAuthServer


class CLI(argparse.ArgumentParser):
    info = ({
        'prog': 'quickbooks-cli',
        'description': 'Starts a local server to handle quickbooks auth',
    })

    def __init__(self):
        super(CLI, self).__init__(**self.info)

        self.add_argument('consumer_key', type=str,
                          help='quickbooks consumer key')
        self.add_argument('consumer_secret', type=str,
                          help='quickbooks consumer secret')
        self.add_argument('-s', '-sandbox', action='store_true',
                          dest='sandbox', help='sandbox flag')
        self.add_argument('-p', '--port', type=int, default=8080,
                          dest='port', help='auth calback port')
        self.add_argument('oauth_version', type=int, default=2,
                          help='OAuth version number')

    def run(self, args=None):
        print('Starting the authentication process...')

        server = QuickBooksAuthServer.build_server(
            args.consumer_key, args.consumer_secret, args.sandbox, args.port, args.oauth_version)

        print('Copy and paste the authorization url on your browser:')
        print(server.qb_data['authorize_url'])

        server.serve_forever()


def cli_execute():
    cli = CLI()
    cli.run(cli.parse_args())


if __name__ == '__main__':
    cli_execute()
