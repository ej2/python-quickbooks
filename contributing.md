# Contributing

I am accepting pull requests. Sometimes life gets busy and it takes me a little while to get everything reviewed and merged in. To help speed up the process, please write tests to cover your changes. I will review/merge them as soon as possible. 

# Testing

I use [pytest](https://docs.pytest.org/en/7.4.x/contents.html), [Coverage](https://coverage.readthedocs.io/en/latest/), and [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) to run the test suite.

*WARNING*: The Tests connect to the QBO API and create/modify/delete data. DO NOT USE A PRODUCTION ACCOUNT!

## Testing setup:

1. Create/login into your [Intuit Developer account](https://developer.intuit.com).
2. On your Intuit Developer account, create a Sandbox company and an App. 
3. Go to the Intuit Developer OAuth 2.0 Playground and fill out the form to get a **refresh token**. You will need to copy the following values into your enviroment variables:
  ```
  export CLIENT_ID="<Client ID>"
  export CLIENT_SECRET="<Client Secret>" 
  export COMPANY_ID="<Realm ID>"  
  export REFRESH_TOKEN="<Refresh token>"
  ```
  
  *Note*: You will need to update the refresh token when it expires. 

5. Install *pytest*, *coverage*, and *pytest-cov*. Using Pip (or whatever):
  `pip install pytest coverage pytest-cov`
  
6. Run all tests: ```pytest  --cov```  
   Run only unit tests: ```pytest tests/unit --cov```   
   Run only integration tests: ```pytest tests/intergration --cov``` 



## Creating new tests
Normal Unit tests that do not connect to the QBO API should be located under `test/unit` Test that connect to QBO API should go under `tests/integration`. Inheriting from `QuickbooksTestCase` will automatically setup `self.qb_client` to use when connecting to QBO.

Example:
```
from tests.integration.test_base import QuickbooksTestCase

class SampleTestCase(QuickbooksTestCase):
  def test_something(self):
    vendors = Vendor.all(max_results=1, qb=self.qb_client)    
```
