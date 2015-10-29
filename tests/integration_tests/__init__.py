import os
from quickbooks.client import QuickBooks


QuickBooks(
    sandbox=True,
    consumer_key=os.environ.get('CONSUMER_KEY'),
    consumer_secret=os.environ.get('CONSUMER_SECRET'),
    access_token=os.environ.get('ACCESS_TOKEN'),
    access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET'),
    company_id=os.environ.get('COMPANY_ID')
)
