import unittest

from quickbooks import QuickBooks
from quickbooks.objects.preferences import Preferences


# Taken from here:
# https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/preferences#full-update-preferences
PAYLOAD = {
  "Preferences": {
    "EmailMessagesPrefs": {
      "InvoiceMessage": {
        "Message": "Your invoice is attached.  Please remit payment at your earliest convenience.\n"
                   "Thank you for your business - we appreciate it very much.\n\nSincerely,\n"
                   "Craig's Design and Landscaping Services",
        "Subject": "Invoice from Craig's Design and Landscaping Services"
      },
      "EstimateMessage": {
        "Message": "Please review the estimate below.  Feel free to contact us if you have any questions.\n"
                   "We look forward to working with you.\n\nSincerely,\nCraig's Design and Landscaping Services",
        "Subject": "Estimate from Craig's Design and Landscaping Services"
      },
      "SalesReceiptMessage": {
        "Message": "Your sales receipt is attached.\nThank you for your business - we appreciate it very much.\n\n"
                   "Sincerely,\nCraig's Design and Landscaping Services",
        "Subject": "Sales Receipt from Craig's Design and Landscaping Services"
      },
      "StatementMessage": {
        "Message": "Your statement is attached.  Please remit payment at your earliest convenience.\n"
                   "Thank you for your business - we appreciate it very much.\n\nSincerely,\n"
                   "Craig's Design and Landscaping Services",
        "Subject": "Statement from Craig's Design and Landscaping Services"
      }
    },
    "ProductAndServicesPrefs": {
      "QuantityWithPriceAndRate": True,
      "ForPurchase": True,
      "QuantityOnHand": True,
      "ForSales": True
    },
    "domain": "QBO",
    "SyncToken": "6",
    "ReportPrefs": {
      "ReportBasis": "Accrual",
      "CalcAgingReportFromTxnDate": False
    },
    "AccountingInfoPrefs": {
      "FirstMonthOfFiscalYear": "January",
      "UseAccountNumbers": True,
      "TaxYearMonth": "January",
      "ClassTrackingPerTxn": False,
      "TrackDepartments": True,
      "TaxForm": "6",
      "CustomerTerminology": "Customers",
      "BookCloseDate": "2018-12-31",
      "DepartmentTerminology": "Location",
      "ClassTrackingPerTxnLine": True
    },
    "SalesFormsPrefs": {
      "ETransactionPaymentEnabled": False,
      "CustomTxnNumbers": False,
      "AllowShipping": False,
      "AllowServiceDate": False,
      "ETransactionEnabledStatus": "NotApplicable",
      "DefaultCustomerMessage": "Thank you for your business and have a great day!",
      "EmailCopyToCompany": False,
      "AllowEstimates": True,
      "DefaultTerms": {
        "value": "3"
      },
      "AllowDiscount": True,
      "DefaultDiscountAccount": "86",
      "AllowDeposit": True,
      "AutoApplyPayments": True,
      "IPNSupportEnabled": False,
      "AutoApplyCredit": True,
      "CustomField": [
        {
          "CustomField": [
            {
              "BooleanValue": False,
              "Type": "BooleanType",
              "Name": "SalesFormsPrefs.UseSalesCustom3"
            },
            {
              "BooleanValue": False,
              "Type": "BooleanType",
              "Name": "SalesFormsPrefs.UseSalesCustom2"
            },
            {
              "BooleanValue": True,
              "Type": "BooleanType",
              "Name": "SalesFormsPrefs.UseSalesCustom1"
            }
          ]
        },
        {
          "CustomField": [
            {
              "StringValue": "Crew #",
              "Type": "StringType",
              "Name": "SalesFormsPrefs.SalesCustomName1"
            }
          ]
        }
      ],
      "UsingPriceLevels": False,
      "ETransactionAttachPDF": False
    },
    "VendorAndPurchasesPrefs": {
      "BillableExpenseTracking": True,
      "TrackingByCustomer": True,
      "POCustomField": [
        {
          "CustomField": [
            {
              "BooleanValue": False,
              "Type": "BooleanType",
              "Name": "PurchasePrefs.UsePurchaseCustom3"
            },
            {
              "BooleanValue": True,
              "Type": "BooleanType",
              "Name": "PurchasePrefs.UsePurchaseCustom2"
            },
            {
              "BooleanValue": True,
              "Type": "BooleanType",
              "Name": "PurchasePrefs.UsePurchaseCustom1"
            }
          ]
        },
        {
          "CustomField": [
            {
              "StringValue": "Sales Rep",
              "Type": "StringType",
              "Name": "PurchasePrefs.PurchaseCustomName2"
            },
            {
              "StringValue": "Crew #",
              "Type": "StringType",
              "Name": "PurchasePrefs.PurchaseCustomName1"
            }
          ]
        }
      ]
    },
    "TaxPrefs": {
      "TaxGroupCodeRef": {
        "value": "2"
      },
      "UsingSalesTax": True
    },
    "OtherPrefs": {
      "NameValue": [
        {
          "Name": "SalesFormsPrefs.DefaultCustomerMessage",
          "Value": "Thank you for your business and have a great day!"
        },
        {
          "Name": "SalesFormsPrefs.DefaultItem",
          "Value": "1"
        },
        {
          "Name": "DTXCopyMemo",
          "Value": "false"
        },
        {
          "Name": "UncategorizedAssetAccountId",
          "Value": "32"
        },
        {
          "Name": "UncategorizedIncomeAccountId",
          "Value": "30"
        },
        {
          "Name": "UncategorizedExpenseAccountId",
          "Value": "31"
        },
        {
          "Name": "SFCEnabled",
          "Value": "true"
        },
        {
          "Name": "DataPartner",
          "Value": "false"
        },
        {
          "Name": "Vendor1099Enabled",
          "Value": "true"
        },
        {
          "Name": "TimeTrackingFeatureEnabled",
          "Value": "true"
        },
        {
          "Name": "FDPEnabled",
          "Value": "false"
        },
        {
          "Name": "ProjectsEnabled",
          "Value": "false"
        },
        {
          "Name": "DateFormat",
          "Value": "Month Date Year separated by a slash"
        },
        {
          "Name": "DateFormatMnemonic",
          "Value": "MMDDYYYY_SEP_SLASH"
        },
        {
          "Name": "NumberFormat",
          "Value": "US Number Format"
        },
        {
          "Name": "NumberFormatMnemonic",
          "Value": "US_NB"
        },
        {
          "Name": "WarnDuplicateCheckNumber",
          "Value": "true"
        },
        {
          "Name": "WarnDuplicateBillNumber",
          "Value": "false"
        },
        {
          "Name": "SignoutInactiveMinutes",
          "Value": "60"
        },
        {
          "Name": "AccountingInfoPrefs.ShowAccountNumbers",
          "Value": "false"
        }
      ]
    },
    "sparse": False,
    "TimeTrackingPrefs": {
      "WorkWeekStartDate": "Monday",
      "MarkTimeEntriesBillable": True,
      "ShowBillRateToAll": False,
      "UseServices": True,
      "BillCustomers": True
    },
    "CurrencyPrefs": {
      "HomeCurrency": {
        "value": "USD"
      },
      "MultiCurrencyEnabled": False
    },
    "Id": "1",
    "MetaData": {
      "CreateTime": "2017-10-25T01:05:43-07:00",
      "LastUpdatedTime": "2018-03-08T13:24:26-08:00"
    }
  },
  "time": "2018-03-12T08:45:52.965-07:00"
}


class PreferencesTests(unittest.TestCase):
    def test_unicode(self):
        preferences = Preferences()
        preferences.Id = 137

        self.assertEquals(str(preferences), "Preferences 137")

    def test_valid_object_name(self):
        preferences = Preferences()
        client = QuickBooks()
        result = client.isvalid_object_name(preferences.qbo_object_name)

        self.assertTrue(result)
        
    def test_structure(self):
        preferences = Preferences.from_json(PAYLOAD['Preferences'])

        print('Expected:', PAYLOAD['Preferences'])
        print('Actual:', preferences.to_dict())
        self.assertEquals(PAYLOAD['Preferences'], preferences.to_dict())
