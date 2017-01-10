python-quickbooks
=================

|Build Status| |Coverage Status|

A Python library for accessing the Quickbooks API. Complete rework of
`quickbooks-python`_.

These instructions were written for a Django application. Make sure to
change it to whatever framework/method you’re using.
You can find additional examples of usage in `Integration tests folder`_.

Connecting your application to Quickbooks Online
------------------------------------------------

1. Create the Authorization URL for your application:

   ::

       from quickbooks import QuickBooks

       client = QuickBooks(
           sandbox=True,
           consumer_key=QUICKBOOKS_CLIENT_KEY,
           consumer_secret=QUICKBOOKS_CLIENT_SECRET,
           callback_url=CALLBACK_URL
       )

       authorize_url = client.get_authorize_url()
       request_token = client.request_token
       request_token_secret = client.request_token_secret

   Store the ``authorize_url``, ``request_token``, and ``request_token_secret``
   for use in the Callback method.

2. Handle the callback:

   ::

       client = QuickBooks(
           sandbox=True,
           consumer_key=QUICKBOOKS_CLIENT_KEY,
           consumer_secret=QUICKBOOKS_CLIENT_SECRET
       )

       client.authorize_url = authorize_url
       client.request_token = request_token
       client.request_token_secret = request_token_secret
       client.set_up_service()

       client.get_access_tokens(request.GET['oauth_verifier'])

       realm_id = request.GET['realmId']
       access_token = client.access_token
       access_token_secret = client.access_token_secret

   Store ``realm_id``, ``access_token``, and ``access_token_secret`` for later use.

Accessing the API
-----------------

Create the QuickBooks client object before you make any calls to QBO. Setup the client
connection using the stored ``access_token`` and the
``access_token_secret`` and ``realm_id``:

::

    from quickbooks import QuickBooks

    client = QuickBooks(
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

::

   client.disconnect_account()

If your consumer_key never changes you can enable the client to stay running:

::

   QuickBooks.enable_global()

You can disable the global client like so:

::

   QuickBooks.disable_global()


List of objects:

::

    
    from quickbooks.objects.customer
    import Customer customers = Customer.all(qb=client)

**Note:** The maximum number of entities that can be returned in a
response is 1000. If the result size is not specified, the default
number is 100. (See `Intuit developer guide`_ for details)

Filtered list of objects:

::

    customers = Customer.filter(Active=True, FamilyName="Smith", qb=client)

Filtered list of objects with paging:

::

    customers = Customer.filter(start_position=1, max_results=25, Active=True, FamilyName="Smith", qb=client)

List Filtered by values in list:

::

    customer_names = ['Customer1', 'Customer2', 'Customer3']
    customers = Customer.choose(customer_names, field="DisplayName", qb=client)

List with custom Where Clause (do not include the “WHERE”):

::

    customers = Customer.where("Active = True AND CompanyName LIKE 'S%'", qb=client)

List with custom Where Clause and paging:

::

    customers = Customer.where("CompanyName LIKE 'S%'", start_position=1, max_results=25, qb=client)

Filtering a list with a custom query (See `Intuit developer guide`_ for
supported SQL statements):

::

    customer = Customer.query("SELECT * FROM Customer WHERE Active = True", qb=client)

Filtering a list with a custom query with paging:

::

    customer = Customer.query("SELECT * FROM Customer WHERE Active = True STARTPOSITION 1 MAXRESULTS 25", qb=client)

Get single object by Id and update:

::

    customer = Customer.get(1, qb=client)
    customer.CompanyName = "New Test Company Name"
    customer.save(qb=client)

Create new object:

::

    customer = Customer()
    customer.CompanyName = "Test Company"
    customer.save(qb=client)

Batch Operations
----------------

The batch operation enables an application to perform multiple
operations in a single request (See `Intuit Batch Operations Guide`_ for
full details).

Batch create a list of objects:

::

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

::

    from quickbooks.batch import batch_update

    customers = Customer.filter(Active=True)

    # Update customer records

    results = batch_update(customers, qb=client)

Batch delete a list of objects:

::

    from quickbooks.batch import batch_delete

    customers = Customer.filter(Active=False)
    results = batch_delete(customers, qb=client)


Review results for batch operation:

::

    # successes is a list of objects that were successfully updated 
    for obj in results.successes:
        print "Updated " + obj.DisplayName

    # faults contains list of failed operations and associated errors
    for fault in results.faults:
        print "Operation failed on " + fault.original_object.DisplayName 
        
        for error in fault.Error:
            print "Error " + error.Message 

Attachments
----------------
See `Attachable documentation`_ for list of valid file types, file size limits and other restrictions.

Attaching a note to a customer:

::

     attachment = Attachable()

     attachable_ref = AttachableRef()
     attachable_ref.EntityRef = customer.to_ref()

     attachment.AttachableRef.append(attachable_ref)

     attachment.Note = 'This is a note'
     attachment.save(qb=client)

Attaching a file to customer:

::

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

::

   account = Account.get(1, qb=client)
   json_data = account.to_json()

Loading JSON data into a quickbooks object:

::

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

::

   date_string = qb_date_format(date(2016, 7, 22))
   date_time_string = qb_datetime_format(datetime(2016, 7, 22, 10, 35, 00))
   date_time_with_utc_string = qb_datetime_utc_offset_format(datetime(2016, 7, 22, 10, 35, 00), '-06:00')


**Note:** Objects and object property names match their Quickbooks
counterparts and do not follow PEP8.

**Note:** This is a work-in-progress made public to help other
developers access the QuickBooks API. Built for a Django project running
on Python 2.

.. _Intuit developer guide: https://developer.intuit.com/docs/0100_accounting/0300_developer_guides/querying_data
.. _Intuit Batch Operations Guide: https://developer.intuit.com/docs/0100_accounting/0300_developer_guides/batch_operations
    
.. _Disconnect documentation: https://developer.intuit.com/docs/0050_quickbooks_api/0020_authentication_and_authorization/oauth_management_api#/Disconnect
.. _quickbooks-python: https://github.com/troolee/quickbooks-python
.. _Minor versions: https://developer.intuit.com/docs/0100_accounting/0300_developer_guides/minor_versions
.. _Attachable documentation: https://developer.intuit.com/docs/api/accounting/Attachable
.. _Integration tests folder: https://github.com/sidecars/python-quickbooks/tree/master/tests/integration

.. |Build Status| image:: https://travis-ci.org/sidecars/python-quickbooks.svg?branch=master
   :target: https://travis-ci.org/sidecars/python-quickbooks
.. |Coverage Status| image:: https://coveralls.io/repos/sidecars/python-quickbooks/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/sidecars/python-quickbooks?branch=master
