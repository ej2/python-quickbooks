python-quickbooks
=================

[![Python package](https://github.com/ej2/python-quickbooks/actions/workflows/python-package.yml/badge.svg)](https://github.com/ej2/python-quickbooks/actions/workflows/python-package.yml)
[![codecov](https://codecov.io/gh/ej2/python-quickbooks/graph/badge.svg?token=AKXS2F7wvP)](https://codecov.io/gh/ej2/python-quickbooks)
[![](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/ej2/python-quickbooks/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/python-quickbooks)](https://pypi.org/project/python-quickbooks/)
 
A Python 3 library for accessing the Quickbooks API. Complete rework of
[quickbooks-python](https://github.com/troolee/quickbooks-python).

These instructions were written for a Django application. Make sure to
change it to whatever framework/method you’re using.
You can find additional examples of usage in [Integration tests folder](https://github.com/ej2/python-quickbooks/tree/master/tests/integration).

For information about contributing, see the [Contributing Page](https://github.com/ej2/python-quickbooks/blob/master/contributing.md).

Installation
------------

```bash
pip install python-quickbooks
```

QuickBooks OAuth
------------------------------------------------

This library requires [intuit-oauth](https://pypi.org/project/intuit-oauth/). 
Follow the [OAuth 2.0 Guide](https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/oauth-2.0) for installation and to get connected to QuickBooks API.


Accessing the API
-----------------

Set up an AuthClient passing in your `CLIENT_ID` and `CLIENT_SECRET`.

    from intuitlib.client import AuthClient

    auth_client = AuthClient(
            client_id='CLIENT_ID',
            client_secret='CLIENT_SECRET',
            access_token='ACCESS_TOKEN',  # If you do not pass this in, the Quickbooks client will call refresh and get a new access token. 
            environment='sandbox',
            redirect_uri='http://localhost:8000/callback',
        )

Then create a QuickBooks client object passing in the AuthClient, refresh token, and company id:

    from quickbooks import QuickBooks

    client = QuickBooks(
            auth_client=auth_client,
            refresh_token='REFRESH_TOKEN',
            company_id='COMPANY_ID',
        )

If you need to access a minor version (See [Minor versions](https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api/minor-versions#working-with-minor-versions) for
details) pass in minorversion when setting up the client:

    client = QuickBooks(
        auth_client=auth_client,
        refresh_token='REFRESH_TOKEN',
        company_id='COMPANY_ID',
        minorversion=69
    )

Object Operations
-----------------

List of objects:

    from quickbooks.objects.customer import Customer
    customers = Customer.all(qb=client)

**Note:** The maximum number of entities that can be returned in a
response is 1000. If the result size is not specified, the default
number is 100. (See [Query operations and syntax](https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api/data-queries) for details)

**Warning:** You should never allow user input to pass into a query without sanitizing it first! This library DOES NOT sanitize user input! 

Filtered list of objects:

    customers = Customer.filter(Active=True, FamilyName="Smith", qb=client)

Filtered list of objects with ordering:

    # Get customer invoices ordered by TxnDate
    invoices = Invoice.filter(CustomerRef='100', order_by='TxnDate', qb=client)

    # Same, but in reverse order
    invoices = Invoice.filter(CustomerRef='100', order_by='TxnDate DESC', qb=client)

    # Order customers by FamilyName then by GivenName
    customers = Customer.all(order_by='FamilyName, GivenName', qb=client)

Filtered list of objects with paging:

    customers = Customer.filter(start_position=1, max_results=25, Active=True, FamilyName="Smith", qb=client)

List Filtered by values in list:

    customer_names = ['Customer1', 'Customer2', 'Customer3']
    customers = Customer.choose(customer_names, field="DisplayName", qb=client)

List with custom Where Clause (do not include the `"WHERE"`):

    customers = Customer.where("Active = True AND CompanyName LIKE 'S%'", qb=client)

  

List with custom Where and ordering

    customers = Customer.where("Active = True AND CompanyName LIKE 'S%'", order_by='DisplayName', qb=client)

List with custom Where Clause and paging:

    customers = Customer.where("CompanyName LIKE 'S%'", start_position=1, max_results=25, qb=client)

Filtering a list with a custom query (See [Query operations and syntax](https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api/data-queries) for
supported SQL statements):

    customers = Customer.query("SELECT * FROM Customer WHERE Active = True", qb=client)

Filtering a list with a custom query with paging:

    customers = Customer.query("SELECT * FROM Customer WHERE Active = True STARTPOSITION 1 MAXRESULTS 25", qb=client)

Get record count (do not include the ``"WHERE"``):

    customer_count = Customer.count("Active = True AND CompanyName LIKE 'S%'", qb=client)

Get single object by Id and update:

    customer = Customer.get(1, qb=client)
    customer.CompanyName = "New Test Company Name"
    customer.save(qb=client)

Create new object:

    customer = Customer()
    customer.CompanyName = "Test Company"
    customer.save(qb=client)

Batch Operations
----------------

The batch operation enables an application to perform multiple
operations in a single request (See [Intuit Batch Operations Guide](https://developer.intuit.com/docs/api/accounting/batch) for
full details).

Batch create a list of objects:

    from quickbooks.batch import batch_create

    customer1 = Customer()
    customer1.CompanyName = "Test Company 1"

    customer2 = Customer()
    customer2.CompanyName = "Test Company 2"

    customers = [customer1, customer2]

    results = batch_create(customers, qb=client)

Batch update a list of objects:

    from quickbooks.batch import batch_update
    customers = Customer.filter(Active=True)

    # Update customer records
    
    results = batch_update(customers, qb=client)

Batch delete a list of objects (only entities that support delete can use batch delete):

    from quickbooks.batch import batch_delete

    payments = Payment.filter(TxnDate=date.today())
    results = batch_delete(payments, qb=client)

Review results for batch operation:

    # successes is a list of objects that were successfully updated
    for obj in results.successes:
       print("Updated " + obj.DisplayName)

    # faults contains list of failed operations and associated errors
    for fault in results.faults:
       print("Operation failed on " + fault.original_object.DisplayName)

       for error in fault.Error:
           print("Error " + error.Message)

Change Data Capture
-----------------------
Change Data Capture returns a list of objects that have changed since a given time 
(see [Change data capture](https://developer.intuit.com/docs/api/accounting/changedatacapture) for more details):

    from quickbooks.cdc import change_data_capture
    from quickbooks.objects import Invoice

    cdc_response = change_data_capture([Invoice], "2017-01-01T00:00:00", qb=client)
    for invoice in cdc_response.Invoice:
       # Do something with the invoice

Querying muliple entity types at the same time:

    from quickbooks.objects import Invoice, Customer
    cdc_response = change_data_capture([Invoice, Customer], "2017-01-01T00:00:00", qb=client)

If you use a `datetime` object for the timestamp, it is automatically converted to a string:

    from datetime import datetime

    cdc_response = change_data_capture([Invoice, Customer], datetime(2017, 1, 1, 0, 0, 0), qb=client)

Attachments
----------------
See [Attachable documentation](https://developer.intuit.com/docs/api/accounting/Attachable) 
for list of valid file types, file size limits and other restrictions.

Attaching a note to a customer:

    attachment = Attachable()

    attachable_ref = AttachableRef()
    attachable_ref.EntityRef = customer.to_ref()

    attachment.AttachableRef.append(attachable_ref)

    attachment.Note = 'This is a note'
    attachment.save(qb=client)

Attaching a file to customer:

    attachment = Attachable()

    attachable_ref = AttachableRef()
    attachable_ref.EntityRef = customer.to_ref()

    attachment.AttachableRef.append(attachable_ref)

    attachment.FileName = 'Filename'
    attachment._FilePath = '/folder/filename'  # full path to file
    attachment.ContentType = 'application/pdf'
    attachment.save(qb=client)

Passing in optional params
----------------
Some QBO objects have options that need to be set on the query string of an API call. 
One example is `include=allowduplicatedocnum` on the Purchase object. You can add these params when calling save:  

    purchase.save(qb=self.qb_client, params={'include': 'allowduplicatedocnum'})

Other operations
----------------
Add Sharable link for an invoice sent to external customers (minorversion must be set to 36 or greater):

    invoice.invoice_link = true


Void an invoice:

    invoice = Invoice()
    invoice.Id = 7
    invoice.void(qb=client)


Working with JSON data
----------------
All objects include `to_json` and `from_json` methods.

Converting an object to JSON data:

    account = Account.get(1, qb=client)
    json_data = account.to_json()

Loading JSON data into a quickbooks object:

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

    date_string = qb_date_format(date(2016, 7, 22))
    date_time_string = qb_datetime_format(datetime(2016, 7, 22, 10, 35, 00))
    date_time_with_utc_string = qb_datetime_utc_offset_format(datetime(2016, 7, 22, 10, 35, 00), '-06:00')

Exception Handling
----------------
The QuickbooksException object contains additional [QBO error code](https://developer.intuit.com/app/developer/qbo/docs/develop/troubleshooting/error-codes#id1) information. 


    from quickbooks.exceptions import QuickbooksException

    try:
        # perform a Quickbooks operation
    except QuickbooksException as e:
        e.message # contains the error message returned from QBO
        e.error_code # contains the  
        e.detail # contains additional information when available  


**Note:** Objects and object property names match their Quickbooks
counterparts and do not follow PEP8.

**Note:** This is a work-in-progress made public to help other
developers access the QuickBooks API. Built for a Django project.



