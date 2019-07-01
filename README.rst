python-quickbooks
=================

|Build Status| |Coverage Status| |License|


A Python library for accessing the Quickbooks API. Complete rework of
`quickbooks-python`_.

These instructions were written for a Django application. Make sure to
change it to whatever framework/method you’re using.
You can find additional examples of usage in `Integration tests folder`_.

For information about contributing, see the `Contributing Page`_.

QuickBooks OAuth
------------------------------------------------

Follow the `OAuth 2.0 Guide`_ to get connected to QuickBooks API.


Accessing the API
-----------------

Set up an AuthClient passing in your ``CLIENT_ID`` and ``CLIENT_SECRET``.

.. code-block:: python


    auth_client = AuthClient(
            client_id='CLIENT_ID',
            client_secret='CLIENT_SECRET',
            environment='sandbox',
            redirect_uri='http://localhost:8000/callback',
        )

Then create a QuickBooks client object passing in the AuthClient, refresh token, and company id:

.. code-block:: python

   from quickbooks import QuickBooks

    client = QuickBooks(
            auth_client=auth_client,
            refresh_token='REFRESH_TOKEN',
            company_id='COMPANY_ID',
        )

If you need to access a minor version (See `Minor versions`_ for
details) pass in minorversion when setting up the client:

.. code-block:: python

    client = QuickBooks(
        auth_client=auth_client,
        refresh_token='REFRESH_TOKEN',
        company_id='COMPANY_ID',
        minorversion=4
    )

Object Operations
-----------------

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

Filtered list of objects with ordering:

.. code-block:: python

    # Get customer invoices ordered by TxnDate
    invoices = Invoice.filter(CustomerRef='100', order_by='TxnDate', qb=client)
    
    # Same, but in reverse order
    invoices = Invoice.filter(CustomerRef='100', order_by='TxnDate DESC', qb=client)
    
    # Order customers by FamilyName then by GivenName
    customers = Customer.all(order_by='FamilyName, GivenName', qb=client)

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

List with custom Where and ordering:

.. code-block:: python

    customers = Customer.where("Active = True AND CompanyName LIKE 'S%'", order_by='DisplayName', qb=client)

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

Other operations
----------------
Void an invoice:

.. code-block:: python

   invoice = Invoice()
   invoice.Id = 7
   invoice.void(qb=client)


If your consumer_key never changes you can enable the client to stay running:

.. code-block:: python

    QuickBooks.enable_global()

You can disable the global client like so:

.. code-block:: python

    QuickBooks.disable_global()


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
.. |License| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://github.com/sidecars/python-quickbooks/blob/master/LICENSE


.. _OAuth 1.0 vs. OAuth 2.0: https://developer.intuit.com/docs/0100_quickbooks_online/0100_essentials/000500_authentication_and_authorization/0010_oauth_1.0a_vs_oauth_2.0_apps

.. _Unable to get Access tokens: https://help.developer.intuit.com/s/question/0D50f00004zqs0ACAQ/unable-to-get-access-tokens
.. _Contributing Page: https://github.com/sidecars/python-quickbooks/wiki/Contributing

.. _OAuth 2.0 Guide: https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/oauth-2.0