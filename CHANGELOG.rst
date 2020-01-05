Changelog
=========

* 0.8.1 (September 18th, 2019)
    * Dropped support for Python 2.7 and 3.3
    * Updated the Invoice to include an AllowOnlineCreditCardPayment attribute.
    * Updated the SendMixin class to url encode input emails.

* 0.8 (June 25th, 2019)
    * Removed support for OAuth 1.0
    * Replace OAuth Session Manager and CLI with intuit-oauth client.
    * Removed disconnect_account and reconnect_account from client.
    * Fixed on Invoice object that caused the DocNumber to be set to an empty string.
    * Added to_ref method to PaymentMethod object.
    * Added CompanyCurrency object.
    * Fixed issue that prevented creation of TaxAgencies.
    * Fixed issues with GroupLine, SubtotalLine, and DescriptionOnlyLine objects.
    * Fixed issue with CDC when there are no changes within a given timestamp.

* 0.7.5 (October 18th, 2018)
    * Fixed bug with reporting authentication failure when attempting to download PDF (previously the error details were "lost").
    * Added refresh_access_tokens to Oauth2SessionManager.
    * Added missing LinkedTxn to Bill object.
    * Added validate_webhook_signature method on client to validate incoming webhooks.
    * Improved exception handling.
    * Updated SendMixin to use 'application/octet-stream' context type.
    * Removed support for Python 2.6.

* 0.7.4 (March 26th, 2018)
    * Fixed bug in SendMixin send method.
    * Added support for send_to email to SendMixin.
    * Removed send_invoice from Invoice object.
    * Removed sandbox from Session Managers.

* 0.7.3 (November 28th, 2017)
    * Fixed bug in ListMixin count method.

* 0.7.1 (November 28th, 2017)
    * Added support for sending invoices.
    * Added count to ListMixin.
    * Fixed issue with PDF file attachments in Python 2.
    * Removed duplicate coverage depnedency.

* 0.7.0 (August 31st, 2017)
    * Added support for OAuth 2.0
    * Added command line interface for connecting to QBO.
    * Fixed unicode issue in 'build_where_clause' and 'where' methods.
    * Fixed incorrectly named field 'PurchaseTaxIncluded' on Item object.
    * Fixed issue with to_ref method on TaxCode.
    * Added DeleteMixin to JournalEntry.
    * Updated User-Agent.

* 0.6.1 (May 9th, 2017)
    * Fixed issue with to_ref method on Bill object.
    * Added DefinitionId to CustomField
    * Update client.py uploads to be Python3 compatible

* 0.6.0 (February 19th, 2017)
    * Added support for Change Data Capture.
    * Added ability to delete objects.
    * Added ToDict to all objects.

* 0.5.7 (January 23rd, 2017)
    * Fixed additional issues downloading PDFs in Python 3
    * Fixed issues caused by hard coded content-type for attachables.

* 0.5.6 (January 18th, 2017)
    * Fixed issue downloading PDFs in Python 3

* 0.5.5 (January 4th, 2017)
    * Imported QuickBooks objects into __init__.py for easier imports
    * Removed duplicate class AttachableRef from deposit.py
    * Removed duplicate class DescriptionLineDetail from journalentry.py
    * Removed duplicate class DescriptionOnlyLine from journalentry.py

* 0.5.4 (November 29th, 2016)
    * Added quickbooks client parameter to QuickbooksPdfDownloadable mixin.

* 0.5.3 (October 14th, 2016)
    * Fixed issue in build_choose_clause and build_where_clause that caused single quotes to not be escaped.

* 0.5.2 (October 14th, 2016)
    * Fixed issue on UpdateMixin.
    * Fixed issue with CashBackInfo.

* 0.5.1 (July 25, 2016)
    * Updated qb_datetime_utc_offset_format to support python 2.6.

* 0.5.0 (July 25, 2016)
    * Added ability to query current user.
    * Added support to reconnect an account.
    * Added to_ref method to Bill object.
    * Added to_ref method to TaxCode.
    * Added date and datetime format helper functions.
    * Fixed issues creating notes with Attachable.
    * Fixed issues with default values on the following objects: Deposit, Employee, Estimate, TimeActivity, Term, Transfer, TaxService and TaxRateDetails
    * Fixed issues that prevented save from working on TaxService.
    * Removed unsupported save method from TaxRate.
    * Removed unsupported save method from TaxCode.
    * Fixed issues loading detail lines on the following objects: JournalEntry, CreditMemo, Bill, Purchase and PurchaseOrder.
    * Removed the following objects: CreditMemoLine, BillLine, JournalEntryLine, PurchaseLine, and PurchaseOrderLine.
    * Corrected spelling of object SaleItemLine to SalesItemLine.


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
