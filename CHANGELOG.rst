Changelog
========

* 0.4.1 (July 22, 2016)
    * Fixed bug on PurchaseLine.
    * Added ability to query current user.
    * Added support to reconnect an account.
    * Added to_ref method to Bill object.
    * Fixed issues creating notes with Attachable.
    * Updated default values on Transfer.
    * Fixed issue with default values on Deposit.
    * Fixed issue with default values on Emloyee.
    * Fixed issue with default vaules on TimeActivity.
    * Added date and datetime format helper functions.

* 0.4.0 (June 15, 2016)
    * Added a way of disconnecting a Quickbooks Account to client.
    * Added support for Quickbooks Reports.
    * Added support for Quickbooks Attachments.
    * Added missing object names to isvalid_object_name.
    * Fixed issue with PurchaseEx on Purchase
    * Removed CompanyInfo from object names used by isvalid_object_name.
    * Changed default of TxnSource to None on the following objects: Deposit, Purchase, RefundReceipt, and Transfer.
    * Changed TxnTaxDetail from a QuickbooksManagedObject to a QuickbooksBaseObject.

* 0.3.13 (May 18, 2016)
    * Added option to enable or disable singeton pattern (it defaults to disabled).
    * Improved error handling.
    * Added missing field CurrencyRef on BillPayment.
    * Fixed issue on TaxRate.
    * Fixed issue with authorize url.

* 0.3.12 (March 18, 2016)
    * Updated field defaults on SalesReceipt object.
    * Updated Id field default on BillLine object.
    * Updated Id field default on DepositLine object.
    * Updated Id field default on PurchaseLine object.
    * Updated Id field default on PurchaseOrderLine object.
    * Added support for downloading PDFs.
    * Added .DS_Store and .idea/ to .gitignore.

* 0.3.11 (February 24, 2016)
    * Updated field defaults on Payment object.
    * Added minor version 4 field to Payment object.
    * Removed invalid fields from PaymentLine object.

* 0.3.10 (February 19, 2016)
    * Updated field defaults on Item object

* 0.3.9 (February 16, 2016)
    * Added missing fields (Country, Note, Line3, Line4, and Line5) to Address object.

* 0.3.8 (February 11, 2016)
    * Updated Budget object to be read only.
    * Added missing fields on CreditMemo object.
    * Changed CreditMemoLine Id to initialize to None.

* 0.3.7 (February 10, 2016)
    * Added missing quickbook object Class

* 0.3.6 (February 3, 2016)
    * Fixed issues with README

* 0.3.5 (February 3, 2016)
    * Added MANIFEST.
    * Converted README to reStructureText.

* 0.3.4 (February 3, 2016)
    * Fixed issues with get_authorize_url.

* 0.2.4 (Sept 13, 2015)
    * Added paging support to "filter", "where", and "all" methods.
