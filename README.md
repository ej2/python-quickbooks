# quickbooks-python
-------------------

A really simple, brute-force, Python class for accessing the Quickbooks API.

It was made to work alongside Django, but should work without it.

Made much simpler with some major contributions from @HaPsantran. See HaPsantran's branch [here](https://github.com/HaPsantran/quickbooks-python). I've cleaned the script up a bit for a semi-clean v0.1.0.

As HaPsantran says in their ReadMe:

>Generally when using this module (or any of the QBO v3 API wrappers out there), keep in mind that there are some glaring omissions in it's functionality that (AFAIK) no one is able to get around programmatically. For example, you can't access (or create, update, or delete, obvi) Deposits or Transfers.

### New in v0.1.1

* Well, versioning :)
* Removed a lot of extraneous method calls that have essentially been replaced with query_object().
* Brought in some pushes from various lovely folks.

## Running the script

Works like any Python module, but you'll need [rauth](http://rauth.readthedocs.org/en/latest/). 

## Getting Access.

1. Make sure you have set up your Quickbooks App. You can check whether you have on their [Manage](https://developer.intuit.com/Application/List) page. If you need help doing that, look at [their documentation](https://developer.intuit.com/docs/0025_quickbooksapi/0010_getting_started/0020_connect/0010_from_within_your_app#Implement_the_OAuth_Authorization_Workflow) <- Have fun, this page only works in Firefox. 

2. When your callback method gets triggered, set up a QuickBooks object, and get a URL for authorization, and then access it:
    ```
    qbObject = QuickBooks(
        consumer_key = QB_OAUTH_CONSUMER_KEY,
        consumer_secret = QB_OAUTH_CONSUMER_SECRET,
        callback_url = QB_OAUTH_CALLBACK_URL,
    )

    authorize_url = qbObject.get_authorize_url() # will create a service, and further set up the qbObject.

    # access URL, however you want to
    ```
3. Access the existing `qbObject`, fetch the `oauth_verifier` and `realmId` from the URL, and set up a session (`request` is Django's [`HttpRequest`](https://docs.djangoproject.com/en/dev/ref/request-response/) object):
    ```
    oauth_token = request.GET['oauth_token']
    oauth_verifier = request.GET['oauth_verifier']
    realm_id = request.GET['realmId']

    session = qbObject.get_access_tokens(oauth_verifier)

    # say you want access to the employees.
    url = "https://qbo.intuit.com/qbo1/"
    url += "resource/employees/v2/%s" % (realm_id)

    r = session.request( #This is just a Rauth request
        "POST", 
        url, 
        header_auth = True, 
        realm = realm_id, 
        params={"format":"json"}
        ) 
    ```
4. Store the `access_token` and the `access_token_secret` and `realm_id`, use them whenever you want to set up a new QB Object:

    ```
    qb = QuickBooks(
        consumer_key = QB_OAUTH_CONSUMER_KEY, 
        consumer_secret = QB_OAUTH_CONSUMER_SECRET,
        access_token = qbtoken.access_token, # the stored token
        access_token_secret = qbtoken.access_token_secret, # the stored secret
        company_id = qbtoken.realm_id #the stored realm_id
        )
    ```
## Accessing the API

Once you've gotten a hold of your QuickBooks access tokens, you can create a QB object:

    qb = QuickBooks(consumer_key = QB_OAUTH_CONSUMER_KEY, 
            consumer_secret = QB_OAUTH_CONSUMER_SECRET,
            access_token = QB_ACCESS_TOKEN, 
            access_token_secret = QB_ACCESS_TOKEN_SECRET,
            company_id = QB_REALM_ID
            )

__Note:__ This is a work-in-progress. It was made public to help other developers access the QuickBooks API, it's not a guarantee that it will ever be finished.

## Available methods

you can access any object via the query_object method.

    qb.query_objects(business_object, params, query_tail)

The available business objects are:

    "Account","Attachable","Bill","BillPayment",
    "Class","CompanyInfo","CreditMemo","Customer",
    "Department","Employee","Estimate","Invoice",
    "Item","JournalEntry","Payment","PaymentMethod",
    "Preferences","Purchase","PurchaseOrder",
    "SalesReceipt","TaxCode","TaxRate","Term",
    "TimeActivity","Vendor","VendorCredit"

Example:

    qb.query_objects("Bill")
    > [{u'DocNumber': ... }]



## From HaPsantran's README
------------------

Update: As I try using the pnl function in report.py, I notice that not all of the activity is making it in. I have to assume it basically doesn't work then. Rather than rebuild it, though, I'm probably going to use other tools outside the  module to massage the ledger_lines I get out of massage.py (rather than build special reporting tools within the quickbooks package).

Intuit has promised reporting features, but who knows...

http://stackoverflow.com/questions/19455750/quickbooks-online-api-financial-data

### License

The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
