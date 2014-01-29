# quickbooks-python
===================

A really simple, brute-force, hacked-together, Python class for accessing the Quickbooks API. 

The API is badly documented and not very flexible, but we've tried to augment that as much as possible. 

Made much simpler with some major contributions from @HaPsantran.

## Accessing the API

Once you've gotten a hold of your QuickBooks access tokens, you can create a QB object:

    qb = QuickBooks(consumer_key = QB_OAUTH_CONSUMER_KEY, 
            consumer_secret = QB_OAUTH_CONSUMER_SECRET,
            access_token = QB_ACCESS_TOKEN, 
            access_token_secret = QB_ACCESS_TOKEN_SECRET,
            company_id = QB_REALM_ID
            )

__Note: the functionality for connecting to the QB API is there as well, I've just not written up proper documentation yet. Have a look at the `get_authorize_url()`, `get_access_tokens()`, and `create_session` methods.__

## Available methods

__Note: This is a work-in-progress. It was made public to help developers access the QuickBooks API, it's not a guarantee that it will ever be finished.__

you can access any object via the query_object method.

    qb.query_object(business_object, params, query_tail)

Some methods have specialized access parameters. These are a bit more explicit.

    qb.fetch_customers()

    qb.fetch_customer(pk)

    qb.fetch_invoices(args**)

Currently only accepts {'query' : {'customer':Id}} as an optional argument. 

    qb.fetch_purchases()

    qb.fetch_journal_entries()

    qb.fetch_bills()

    qb.chart_of_accounts()

    qb.quick_report()

    qb.ledgerize()