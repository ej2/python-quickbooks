python-quickbooks
=================

|Build Status| |Coverage Status|


A Python library for accessing the Quickbooks API. Complete rework of
`quickbooks-python`_.

These instructions were written for a Django application. Make sure to
change it to whatever framework/method you’re using.
You can find additional examples of usage in `Integration tests folder`_.

QuickBooks OAuth
------------------------------------------------

As of July 17, 2017, all new applications connecting to QuickBook Online must use OAuth 2.0.
Existing applications can continue to use OAuth 1.0 (See `OAuth 1.0 vs. OAuth 2.0`_ for details)


Connecting your application with quickbooks-cli
-------------------

From the command line, call quickbooks-cli tool passing in either your consumer_key and consumer_secret (OAuth 1.0)
or your client_id and client_secret (OAuth 2.0), plus the OAuth version number:

.. code-block:: console

    quickbooks-cli [-h] [-s] [-p PORT] consumer_key consumer_secret oauth_version


Manually connecting with OAuth version 1.0
--------

1. Create the Authorization URL for your application:

.. code-block:: python

       from quickbooks import Oauth1SessionManager

       session_manager = Oauth1SessionManager(
           sandbox=True,
           consumer_key=QUICKBOOKS_CLIENT_KEY,
           consumer_secret=QUICKBOOKS_CLIENT_SECRET,
       )

       callback_url = 'http://localhost:8000'  # Quickbooks will send the response to this url
       authorize_url = session_manager.get_authorize_url(callback_url)
       request_token = session_manager.request_token
       request_token_secret = session_manager.request_token_secret

Store the ``authorize_url``, ``request_token``, and ``request_token_secret``
for use in the Callback method.

2. Redirect to the ``authorize_url``. Quickbooks will redirect back to your callback_url.
3. Handle the callback:

.. code-block:: python

       session_manager = Oauth1SessionManager(
           sandbox=True,
           consumer_key=QUICKBOOKS_CLIENT_KEY,
           consumer_secret=QUICKBOOKS_CLIENT_SECRET
       )

       session_manager.authorize_url = authorize_url
       session_manager.request_token = request_token
       session_manager.request_token_secret = request_token_secret

       session_manager.get_access_tokens(request.GET['oauth_verifier'])

       realm_id = request.GET['realmId']
       access_token = session_manager.access_token
       access_token_secret = session_manager.access_token_secret

Store ``realm_id``, ``access_token``, and ``access_token_secret`` for later use.


Manually connecting with OAuth version 2.0
--------

1. Create the Authorization URL for your application:

.. code-block:: python

       from quickbooks import Oauth2SessionManager

       session_manager = Oauth2SessionManager(
           sandbox=True,
           client_id=QUICKBOOKS_CLIENT_ID,
           client_secret=QUICKBOOKS_CLIENT_SECRET,
           base_url='http://localhost:8000',
       )

       callback_url = 'http://localhost:8000'  # Quickbooks will send the response to this url
       authorize_url = session_manager.get_authorize_url(callback_url)


2. Redirect to the ``authorize_url``. Quickbooks will redirect back to your callback_url.
3. Handle the callback:

.. code-block:: python

       session_manager = Oauth2SessionManager(
           sandbox=True,
           client_id=QUICKBOOKS_CLIENT_ID,
           client_secret=QUICKBOOKS_CLIENT_SECRET,
           base_url='http://localhost:8000',
       )

       session_manager.get_access_tokens(request.GET['code'])
       access_token = session_manager.access_token

Store ``access_token`` for later use.

Accessing the API
-----------------

Set up an OAuth session manager to pass to the QuickBooks client.
OAuth version 1.0 - Setup the session manager using the stored ``access_token`` and the
``access_token_secret`` and ``realm_id``:

.. code-block:: python

        session_manager = Oauth1SessionManager(
            sandbox=True,
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET,
        )

OAuth version 2.0 - Setup the session manager using the stored ``access_token`` and ``realm_id``:

.. code-block:: python

        self.session_manager = Oauth2SessionManager(
            sandbox=True,
            client_id=realm_id,
            client_secret=CLIENT_SECRET,
            access_token=AUTH2_ACCESS_TOKEN,
        )

Then create the QuickBooks client object passing in the session manager:

.. code-block:: python

   from quickbooks import QuickBooks

    client = QuickBooks(
        sandbox=True,
        session_manager=session_manager,
        company_id=realm_id
    )

If you need to access a minor version (See `Minor versions`_ for
details) pass in minorversion when setting up the client:

.. code-block:: python

    client = QuickBooks(
        sandbox=True,
        consumer_key=QUICKBOOKS_CLIENT_KEY,
        consumer_secret=QUICKBOOKS_CLIENT_SECRET,
        access_token=access_token,
        access_token_secret=access_token_secret,
        company_id=realm_id,
        minorversion=4
    )

You can disconnect the current Quickbooks Account like so (See `Disconnect documentation`_ for full details):

.. code-block:: python

    client.disconnect_account()

If your consumer_key never changes you can enable the client to stay running:

.. code-block:: python

    QuickBooks.enable_global()

You can disable the global client like so:

.. code-block:: python

    QuickBooks.disable_global()


List of objects:

.. code-block:: python

    from quickbooks.objects.customer import Customer
    customers = Customer.all(qb=client)

**Note:** The maximum number of entities that can be returned in a
response is 1000. If the result size is not specified, the default
number is 100. (See `Intuit developer guide`_ for details)

Filtered list of objects:

.. code-block:: python

    customers = Customer.filter(Active=True, FamilyName="Smith", qb=client)

Filtered list of objects with paging:

.. code-block:: python

    customers = Customer.filter(start_position=1, max_results=25, Active=True, FamilyName="Smith", qb=client)

List Filtered by values in list:

.. code-block:: python

    customer_names = ['Customer1', 'Customer2', 'Customer3']
    customers = Customer.choose(customer_names, field="DisplayName", qb=client)

List with custom Where Clause (do not include the ``"WHERE"``):

.. code-block:: python

    customers = Customer.where("Active = True AND CompanyName LIKE 'S%'", qb=client)

List with custom Where Clause and paging:

.. code-block:: python

    customers = Customer.where("CompanyName LIKE 'S%'", start_position=1, max_results=25, qb=client)

Filtering a list with a custom query (See `Intuit developer guide`_ for
supported SQL statements):

.. code-block:: python

    customers = Customer.query("SELECT * FROM Customer WHERE Active = True", qb=client)

Filtering a list with a custom query with paging:

.. code-block:: python

    customers = Customer.query("SELECT * FROM Customer WHERE Active = True STARTPOSITION 1 MAXRESULTS 25", qb=client)

Get record count (do not include the ``"WHERE"``):

.. code-block:: python

    customer_count = Customer.count("Active = True AND CompanyName LIKE 'S%'", qb=client)

Get single object by Id and update:

.. code-block:: python

    customer = Customer.get(1, qb=client)
    customer.CompanyName = "New Test Company Name"
    customer.save(qb=client)

Create new object:

.. code-block:: python

    customer = Customer()
    customer.CompanyName = "Test Company"
    customer.save(qb=client)

Batch Operations
----------------

The batch operation enables an application to perform multiple
operations in a single request (See `Intuit Batch Operations Guide`_ for
full details).

Batch create a list of objects:

.. code-block:: python

    from quickbooks.batch import batch_create

    customer1 = Customer()
    customer1.CompanyName = "Test Company 1"

    customer2 = Customer()
    customer2.CompanyName = "Test Company 2"

    customers = []
    customers.append(customer1)
    customers.append(customer2)

    results = batch_create(customers, qb=client)

Batch update a list of objects:

.. code-block:: python

   from quickbooks.batch import batch_update

   customers = Customer.filter(Active=True)

   # Update customer records

   results = batch_update(customers, qb=client)

Batch delete a list of objects:

.. code-block:: python

   from quickbooks.batch import batch_delete

   customers = Customer.filter(Active=False)
   results = batch_delete(customers, qb=client)

Review results for batch operation:

.. code-block:: python

   # successes is a list of objects that were successfully updated 
   for obj in results.successes:
       print "Updated " + obj.DisplayName

   # faults contains list of failed operations and associated errors
   for fault in results.faults:
       print "Operation failed on " + fault.original_object.DisplayName 

       for error in fault.Error:
           print "Error " + error.Message 

Change Data Capture
-----------------------
Change Data Capture returns a list of objects that have changed since a given time (see `Change data capture`_ for more
details):

.. code-block:: python

   from quickbooks.cdc import change_data_capture
   from quickbooks.objects import Invoice

   cdc_response = change_data_capture([Invoice], "2017-01-01T00:00:00", qb=client)
   for invoice in cdc_response.Invoice:
       # Do something with the invoice

Querying muliple entity types at the same time:

.. code-block:: python

   from quickbooks.objects import Invoice, Customer

   cdc_response = change_data_capture([Invoice, Customer], "2017-01-01T00:00:00", qb=client)


If you use a ``datetime`` object for the timestamp, it is automatically converted to a string:

.. code-block:: python

   from datetime import datetime

   cdc_response = change_data_capture([Invoice, Customer], datetime(2017, 1, 1, 0, 0, 0), qb=client)

Attachments
----------------
See `Attachable documentation`_ for list of valid file types, file size limits and other restrictions.

Attaching a note to a customer:

.. code-block:: python

    attachment = Attachable()

    attachable_ref = AttachableRef()
    attachable_ref.EntityRef = customer.to_ref()

    attachment.AttachableRef.append(attachable_ref)

    attachment.Note = 'This is a note'
    attachment.save(qb=client)

Attaching a file to customer:

.. code-block:: python

    attachment = Attachable()

    attachable_ref = AttachableRef()
    attachable_ref.EntityRef = customer.to_ref()

    attachment.AttachableRef.append(attachable_ref)

    attachment.FileName = 'Filename'
    attachment._FilePath = '/folder/filename'  # full path to file
    attachment.ContentType = 'application/pdf'
    attachment.save(qb=client)

Working with JSON data
----------------
All objects include ``to_json`` and ``from_json`` methods.

Converting an object to JSON data:

.. code-block:: python

   account = Account.get(1, qb=client)
   json_data = account.to_json()

Loading JSON data into a quickbooks object:

.. code-block:: python

   account = Account()
   account.from_json(
     {
      "AccountType": "Accounts Receivable",
      "Name": "MyJobs"
     }
   )
   account.save(qb=client)

Date formatting
----------------
When setting date or datetime fields, Quickbooks requires a specific format.
Formating helpers are available in helpers.py. Example usage:

.. code-block:: python

   date_string = qb_date_format(date(2016, 7, 22))
   date_time_string = qb_datetime_format(datetime(2016, 7, 22, 10, 35, 00))
   date_time_with_utc_string = qb_datetime_utc_offset_format(datetime(2016, 7, 22, 10, 35, 00), '-06:00')


**Note:** Objects and object property names match their Quickbooks
counterparts and do not follow PEP8.

**Note:** This is a work-in-progress made public to help other
developers access the QuickBooks API. Built for a Django project running
on Python 2.

.. _Intuit developer guide: https://developer.intuit.com/docs/0100_accounting/0300_developer_guides/querying_data
.. _Intuit Batch Operations Guide: https://developer.intuit.com/docs/api/accounting/batch
    
.. _Disconnect documentation: https://developer.intuit.com/docs/0050_quickbooks_api/0020_authentication_and_authorization/oauth_management_api#/Disconnect
.. _quickbooks-python: https://github.com/troolee/quickbooks-python
.. _Minor versions: https://developer.intuit.com/docs/0100_quickbooks_online/0200_dev_guides/accounting/minor_versions
.. _Attachable documentation: https://developer.intuit.com/docs/api/accounting/Attachable
.. _Integration tests folder: https://github.com/sidecars/python-quickbooks/tree/master/tests/integration
.. _Change data capture: https://developer.intuit.com/docs/api/accounting/changedatacapture


.. |Build Status| image:: https://travis-ci.org/sidecars/python-quickbooks.svg?branch=master
   :target: https://travis-ci.org/sidecars/python-quickbooks
.. |Coverage Status| image:: https://coveralls.io/repos/sidecars/python-quickbooks/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/sidecars/python-quickbooks?branch=master

.. _OAuth 1.0 vs. OAuth 2.0: https://developer.intuit.com/docs/0100_quickbooks_online/0100_essentials/000500_authentication_and_authorization/0010_oauth_1.0a_vs_oauth_2.0_apps