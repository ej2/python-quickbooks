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

**Note:** Objects and object property names match their Quickbooks
counterparts and do not follow PEP8.

**Note:** This is a work-in-progress made public to help other
developers access the QuickBooks API. Built for a Django project running
on Python 2.

.. _Intuit developer guide: https://developer.intuit.com/docs/0100_accounting/0300_developer_guides/querying_data
.. _Intuit Batch Operations Guide: https://developer.intuit.com/docs/0100_accounting/0300_developer_guides/batch_operations
    

.. _quickbooks-python: https://github.com/troolee/quickbooks-python
.. _Minor versions: https://developer.intuit.com/docs/0100_accounting/0300_developer_guides/minor_versions

.. |Build Status| image:: https://travis-ci.org/sidecars/python-quickbooks.svg?branch=master
   :target: https://travis-ci.org/sidecars/python-quickbooks
.. |Coverage Status| image:: https://coveralls.io/repos/sidecars/python-quickbooks/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/sidecars/python-quickbooks?branch=master
