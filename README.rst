python-quickbooks
=================

|Build Status| |Coverage Status|

A Python library for accessing the Quickbooks API. Complete rework of
`quickbooks-python`_.

These instructions were written for a Django application. Make sure to
change it to whatever framework/method you’re using.

Connecting your application to Quickbooks Online
------------------------------------------------

1. Create the Authorization URL for your application:

   ::

       from quickbooks import QuickBooks

       quickbooks = QuickBooks(
           sandbox=True,
           consumer_key=QUICKBOOKS_CLIENT_KEY,
           consumer_secret=QUICKBOOKS_CLIENT_SECRET,
           callback_url=CALLBACK_URL
       )

       authorize_url = quickbooks.get_authorize_url()

   Store the authorize\_url, request\_token, and request\_token\_secret
   for use in the Callback method.

2. Handle the callback:

   ::

       quickbooks = QuickBooks(
           sandbox=True,
           consumer_key=QUICKBOOKS_CLIENT_KEY,
           consumer_secret=QUICKBOOKS_CLIENT_SECRET,
           callback_url=CALLBACK_URL
       )

       quickbooks.authorize_url = authorize_url
       quickbooks.request_token = request_token
       quickbooks.request_token_secret = request_token_secret
       quickbooks.set_up_service()

       quickbooks.get_access_tokens(request.GET['oauth_verifier'])

       realm_id = request.GET['realmId']
       access_token = quickbooks.access_token
       access_token_secret = quickbooks.access_token_secret

   Store realm\_id, access\_token, and access\_token\_secret need to be
   stored for later use.

Accessing the API
-----------------

QuickBooks client uses a singleton pattern. Just be sure to create the
QuickBooks object before you make any calls to QBO. Setup the client
connection using the stored ``access_token`` and the
``access_token_secret`` and ``realm_id``:

::

    from quickbooks import QuickBooks

    QuickBooks(
        sandbox=True,
        consumer_key=QUICKBOOKS_CLIENT_KEY,
        consumer_secret=QUICKBOOKS_CLIENT_SECRET,
        access_token=access_token,
        access_token_secret=access_token_secret,
        company_id=realm_id
    )

If you need to access a minor version (See `Minor versions`_ for
details) pass in minorversion when setting up the client:

::

    QuickBooks(
        sandbox=True,
        consumer_key=QUICKBOOKS_CLIENT_KEY,
        consumer_secret=QUICKBOOKS_CLIENT_SECRET,
        access_token=access_token,
        access_token_secret=access_token_secret,
        company_id=realm_id,
        minorversion=4
    )

List of objects:

::

    from quickbooks.objects.customer import Customer
    cu

.. _quickbooks-python: https://github.com/troolee/quickbooks-python
.. _Minor versions: https://developer.intuit.com/docs/0100_accounting/0300_developer_guides/minor_versions

.. |Build Status| image:: https://travis-ci.org/sidecars/python-quickbooks.svg?branch=master
   :target: https://travis-ci.org/sidecars/python-quickbooks
.. |Coverage Status| image:: https://coveralls.io/repos/sidecars/python-quickbooks/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/sidecars/python-quickbooks?branch=master