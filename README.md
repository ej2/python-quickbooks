# python-quickbooks
-------------------

A Python library for accessing the Quickbooks API. 
Complete rework of [quickbooks-python](https://github.com/troolee/quickbooks-python).

These instructions were written for a Django application. Make sure to change it to whatever framework/method you're using. 

## Connecting your application to Quickbooks Online

1. Create the Authorization URL for your application:

        from quickbooks import QuickBooks
        
        quickbooks = QuickBooks(
            sandbox=True,
            consumer_key=QUICKBOOKS_CLIENT_KEY,
            consumer_secret=QUICKBOOKS_CLIENT_SECRET,
            callback_url=CALLBACK_URL
        )

        authorize_url = quickbooks.get_authorize_url()

    Store the authorize_url, request_token, and request_token_secret for use in the Callback method.

2. Handle the callback:

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

    Store realm_id, access_token, and access_token_secret need to be stored for later use.


## Accessing the API

QuickBooks client uses a singleton pattern. Just be sure to create the QuickBooks object before you make any calls to QBO.
Setup the client connection using the stored `access_token` and the `access_token_secret` and `realm_id`:

    from quickbooks import QuickBooks

    QuickBooks(
        sandbox=True,
        consumer_key=QUICKBOOKS_CLIENT_KEY,
        consumer_secret=QUICKBOOKS_CLIENT_SECRET,
        access_token=access_token,
        access_token_secret=access_token_secret,
        company_id=realm_id
    )


List of objects:

    from quickbooks.object.customer import Customer
    customers = Customer.all()


Filtered list of objects (filtering currently only supports simple queries):


    customers = Customer.filter(Active=True)


Get single object by Id and update:


    customer = Customer.get(1)
    customer.CompanyName = "New Test Company Name"
    customer.save()


Create new object:


    customer = Customer()
    customer.CompanyName = "Test Company"
    customer.save()



__Note:__ This is a work-in-progress made public to help other developers access the QuickBooks API. 
Built for a Django project running on Python 2. It has not been tested with Python 3.


