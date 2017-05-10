import argparse

from quickbooks.tools.auth import handle_auth


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

    def run(self, args=None):
        handle_auth(args.consumer_key, args.consumer_secret,
                    args.sandbox, args.port)


def cli_execute():
    cli = CLI()
    cli.run(cli.parse_args())


if __name__ == '__main__':
    cli_execute()
