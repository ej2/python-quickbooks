"""
These are intended to be helpful references that will take up a lot of
space if included in the main modules, so I'm breaking them out into
a separate module...maybe some utility functions will be in order at some point,
such as figuring out which attributes all elements have in common, etc.

https://developer.intuit.com/docs/0025_quickbooksapi/
    0050_data_services/030_entity_services_reference/account

"""

BUSINESS_OBJECTS = ["Account","Attachable","Bill","BillPayment",
                    "Class","CompanyInfo","CreditMemo","Customer",
                    "Department","Employee","Estimate","Invoice",
                    "Item","JournalEntry","Payment","PaymentMethod",
                    "Preferences","Purchase","PurchaseOrder",
                    "SalesReceipt","TaxCode","TaxRate","Term",
                    "TimeActivity","Vendor","VendorCredit"]

OBJECT_ATTRIBUTES = {

    "Account" : [

        "Id", "SyncToken", "MetaData", "Name", "SubAccount",
        "ParentRef", "Description", "FullyQualifiedName", "Active",
        "Classification", "AccountType", "AccountSubType", "AcctNum",
        "OpeningBalance", "OpeningBalanceDate", "CurrentBalance",
        "CurentBalanceWithSubAccounts", "CurrencyRef"],

    "Class" :[

        "Id", "SyncToken", "MetaData", "Name", "SubClass", "ParentRef",
        "FullyQualifiedName", "Active"],

    "Customer" :[

        "Id", "SyncToken", "MetaData", "Title", "GivenName", "MiddleName",
        "FamilyName", "Suffix", "FullyQualifiedName", "CompanyName",
        "DisplayName", "PrintOnCheckName", "Active", "PrimaryPhone",
        "AlternatePhone", "Mobile", "Fax", "PrimaryEmailAddr", "WebAddr",
        "DefaultTaxCodeRef", "Taxable", "BillAddr", "ShipAddr", "Notes",
        "Job", "BillWithParent", "ParentRef", "Level", "SalesTermRef",
        "PaymentMethodRef", "Balance", "OpenBalanceDate", "BalanceWithJobs",
        "CurrencyRef", "PreferredDeliveryMethod", "ResaleNum"],

    "Department" :[

        "Id", "SyncToken", "MetaData", "Name", "SubDepartment",
        "ParentRef", "FullyQualifiedName", "Active"],

    "Employee" :[

        "Id", "SyncToken", "MetaData", "Organization", "Title",
        "GivenName", "MiddleName", "FamilyName", "Suffix", "DisplayName",
        "PrintOnCheckName", "Active", "PrimaryPhone", "Mobile",
        "PrimaryPhone", "EmployeeNumber", "SSN", "PrimaryAddr",
        "BillableTime", "BillRate", "BirthDate", "Gender", "HiredDate",
        "ReleasedDate"],

    "Item" :[

        "Id", "SyncToken", "MetaData", "Name", "Description", "Active",
        "SubItem", "ParentRef", "Level", "FullyQualifiedName", "Taxable",
        "SalesTaxIncluded", "UnitPrice", "RatePercent", "Type", 
        "IncomeAccountRef", "PurchaseDesc", "PurchaseTaxIncluded",
        "PurchaseCost", "ExpenseAccountRef", "AssetAccountRef",
        "TrackQtyOnHand", "QtyOnHand", "SalesTaxCodeRef",
        "PurchaseTaxCodeRef", "InvStartDate"],

    "PaymentMethod" :[

        #note that the CustomField attribute can (and maybe MUST) be
        #subscripted...

        "Id", "SyncToken", "MetaData", "CustomField", "AttachableRef",
        "Name", "Active", "Type"],

    "TaxCode" :[

        #note that SalesTaxRateList has sub-attribute TaxRateDetail,
        #which itself must be subscripted and those sub-attributes have
        #their own sub-attributes TaxRateRef, TaxRateApplicable,
        #and TaxOrder
        #The same is true of PurchaseTaxRateList (apparently only for
        #VAT-charging countries, which excludes the U.S.)

        "Id", "SyncToken", "MetaData", "Name", "Description", "Active",
        "Taxable", "TaxGroup", "SalesTaxRateList", "PurchaseTaxRateList"],

    "TaxRate":[

        "Id", "SyncToken", "MetaData", "Name", "Description", "Active", 
        "RateValue", "AgencyRef", "TaxReturnLineRef", "SpecialTaxType",
        "DisplayType", "EffectiveTaxRate"],

    "Term" :[

        #note that the CustomField attribute can (and maybe MUST) be
        #subscripted...

        "Id", "SyncToken", "MetaData", "CustomField", "AttachableRef",
        "Name", "Active", "Type", "DiscountPercent", "DueDays",
        "DiscountDays", "DayOfMonthDue", "DueNextMonthDays",
        "DiscountDayOfMonth"],

    "Vendor" :[

        #note that the OtherContactInfo attribute can (and maybe MUST) be
        #subscripted...

        "Id", "SyncToken", "MetaData", "Title", "GiveName", "MiddleName",
        "FamilyName", "Suffix", "CompanyName", "DisplayName",
        "PrintOnCheckName", "Active", "PrimaryPhone", "AlternatePhone",
        "Mobile", "Fax", "PrimaryEmailAddr", "WebAddr", "BillAddr",
        "OtherContactInfo", "TaxIdentifier", "TaxIdentifier", "TermRef",
        "Balance", "AcctNum", "Vendor1099", "CurrencyRef"]

}



#we may find it useful to sort AccountTypes in trial balance order

transaction_objects = [

     "Bill", "BillPayment", "CreditMemo", "Estimate", "Invoice",
     "JournalEntry", "Payment", "Purchase", "PurchaseOrder", 
     "SalesReceipt", "TimeActivity", "VendorCredit"

 ]

name_list_objects = [

     "Account", "Class", "Customer", "Department", "Employee", "Item",
     "PaymentMethod", "TaxCode", "TaxRate", "Term", "Vendor"

 ]


tb_type_order = [
    "Bank", "Accounts Receivable", "Other Current Asset",
    "Fixed Asset", "Other Asset",
    "Accounts Payable", "Credit Card", "Long Term Liability",
    "Other Current Liability",
    "Equity",
    "Income", "Other Income",
    "Cost of Goods Sold", "Expense", "Other Expense"
]        

#Linked_Txn's have TxnType's that map to specific qbbo types
linked_txn_correction = {
    "Bill"               : "Bill",
    "Check"              : "Purchase",
    "Credit Card Credit" : "Purchase",
    "Invoice"            : "Invoice",
    "Journal Entry"      : "JournalEntry"
}

"""
Notes:

QBO will NOT let the user enter a bill with a negative total amount.

"""

#prototypical entries for new entry creation:

"""
Here's a JournalEntry:

{
    "DocNumber": "MyJEnum", 
    "SyncToken": "3", 
    "domain": "QBO", 
    "TxnDate": "2014-02-08", 
    "CurrencyRef": {
        "name": "United States Dollar", 
        "value": "USD"
    }, 
    "PrivateNote": "test document-level memo", 
    "sparse": false, 
    "Line": [
        {
            "JournalEntryLineDetail": {
                "DepartmentRef": {
                    "name": "Business Unit A", 
                    "value": "3"
                }, 
                "PostingType": "Credit", 
                "AccountRef": {
                    "name": "Miscellaneous Income", 
                    "value": "57"
                }, 
                "ClassRef": {
                    "name": "Class A", 
                    "value": "3200000000000365067"
                }, 
                "Entity": {
                    "Type": "Customer", 
                    "EntityRef": {
                        "name": "Paypal Sender", 
                        "value": "7"
                    }
                }
            }, 
            "DetailType": "JournalEntryLineDetail", 
            "Amount": 1.23, 
            "Id": "0", 
            "Description": "Test Line 0 Description"
        }, 
        {
            "JournalEntryLineDetail": {
                "DepartmentRef": {
                    "name": "Business Unit B", 
                    "value": "4"
                }, 
                "PostingType": "Debit", 
                "AccountRef": {
                    "name": "6240 Miscellaneous", 
                    "value": "29"
                }, 
                "ClassRef": {
                    "name": "Class B", 
                    "value": "3200000000000365068"
                }, 
                "Entity": {
                    "Type": "Vendor", 
                    "EntityRef": {
                        "name": "Paypal Recipient", 
                        "value": "52"
                    }
                }
            }, 
            "DetailType": "JournalEntryLineDetail", 
            "Amount": 4.56, 
            "Id": "1", 
            "Description": "Test Line 1 Description"
        }, 
        {
            "JournalEntryLineDetail": {
                "PostingType": "Credit", 
                "AccountRef": {
                    "name": "Other Liabilities", 
                    "value": "71"
                }, 
                "Entity": {
                    "Type": "Customer", 
                    "EntityRef": {
                        "name": "Owner", 
                        "value": "190"
                    }
                }
            }, 
            "DetailType": "JournalEntryLineDetail", 
            "Amount": 3.33, 
            "Id": "2", 
            "Description": "Test Line 2 Description"
        }
    ], 
    "Adjustment": false, 
    "Id": "1065", 
    "MetaData": {
        "CreateTime": "2014-02-08T07:52:16-08:00", 
        "LastUpdatedTime": "2014-02-08T08:05:29-08:00"
    }
}
"""

"""
Here's a Customer
{
    "domain": "QBO", 
    "FamilyName": "Customer", 
    "DisplayName": "Mr. Test This Customer, Jr", 
    "Title": "Mr.", 
    "PreferredDeliveryMethod": "Print", 
    "PrimaryEmailAddr": {
        "Address": "testcustomer@gmail.com"
    }, 
    "BillAddr": {
        "City": "New York", 
        "Country": "United States", 
        "Line1": "123 w. 45th st.", 
        "PostalCode": "10036", 
        "Lat": "40.7573863", 
        "Long": "-73.9836904", 
        "CountrySubDivisionCode": "NY", 
        "Id": "72"
    }, 
    "ResaleNum": "xyz", 
    "GivenName": "Test", 
    "SalesTermRef": {
        "value": "10"
    }, 
    "FullyQualifiedName": "Test Custy Two:Mr. Test This Customer, Jr", 
    "Fax": {
        "FreeFormNumber": "(414) 555-1212"
    }, 
    "BillWithParent": true, 
    "Mobile": {
        "FreeFormNumber": "(313) 555-1212"
    }, 
    "Job": true, 
    "BalanceWithJobs": 0, 
    "PrimaryPhone": {
        "FreeFormNumber": "(212) 555-1212"
    }, 
    "Taxable": true, 
    "AlternatePhone": {
        "FreeFormNumber": "sumfing"
    }, 
    "MetaData": {
        "CreateTime": "2014-02-11T22:31:46-08:00", 
        "LastUpdatedTime": "2014-02-11T22:34:02-08:00"
    }, 
    "ParentRef": {
        "value": "192"
    }, 
    "Level": 1, 
    "MiddleName": "This", 
    "Notes": "Here's some other details!", 
    "WebAddr": {
        "URI": "http://www.testcustomer.com"
    }, 
    "Active": true, 
    "Balance": 0, 
    "SyncToken": "2", 
    "PaymentMethodRef": {
        "value": "16"
    }, 
    "Suffix": "Jr", 
    "CompanyName": "Test Customer's Company, Inc.", 
    "ShipAddr": {
        "City": "New York", 
        "Country": "USA", 
        "Line1": "678 W. 90th St.", 
        "PostalCode": "10036", 
        "Lat": "40.7921586", 
        "Long": "-73.9777118", 
        "CountrySubDivisionCode": "NY", 
        "Id": "73"
    }, 
    "PrintOnCheckName": "Mr. Test This Customer, Jr", 
    "sparse": false, 
    "Id": "191"
}
"""

"""
Here's a Vendor
{
    "domain": "QBO", 
    "PrimaryEmailAddr": {
        "Address": "testvendor@gmail.com"
    }, 
    "DisplayName": "Miss Test That Vendor, Sr", 
    "Title": "Miss", 
    "TermRef": {
        "value": "9"
    }, 
    "GivenName": "Test", 
    "Fax": {
        "FreeFormNumber": "(717) 555-1212"
    }, 
    "Mobile": {
        "FreeFormNumber": "(616) 555-1212"
    }, 
    "PrimaryPhone": {
        "FreeFormNumber": "(515) 555-1212"
    }, 
    "Active": true, 
    "AlternatePhone": {
        "FreeFormNumber": "What's this?"
    }, 
    "MetaData": {
        "CreateTime": "2014-02-11T22:38:08-08:00", 
        "LastUpdatedTime": "2014-02-11T22:38:09-08:00"
    }, 
    "Vendor1099": true, 
    "BillAddr": {
        "City": "New York", 
        "Country": "USA", 
        "Line1": "987 E. 65th St.", 
        "PostalCode": "98765", 
        "Lat": "40.6300376", 
        "Long": "-74.0082039", 
        "CountrySubDivisionCode": "Ny", 
        "Id": "74"
    }, 
    "MiddleName": "That", 
    "WebAddr": {
        "URI": "http://www.testvendor.com"
    }, 
    "Balance": 45.23, 
    "SyncToken": "0", 
    "Suffix": "Sr", 
    "CompanyName": "Test Vendor's Company", 
    "FamilyName": "Vendor", 
    "TaxIdentifier": "123-45-6789", 
    "AcctNum": "56A", 
    "PrintOnCheckName": "Some Other Name for Test Vendor", 
    "sparse": false, 
    "Id": "194"
}
"""

"""
Here's an Employee 
{
    "domain": "QBO", 
    "PrimaryEmailAddr": {
        "Address": "working@foryoudude.com"
    }, 
    "DisplayName": "Mr Working For You, Dude", 
    "Title": "Mr", 
    "BillableTime": true, 
    "GivenName": "Working", 
    "BirthDate": "1945-01-23", 
    "Mobile": {
        "FreeFormNumber": "(919) 555-1212"
    }, 
    "PrintOnCheckName": "Mr Working For You, Duder",
    "PrimaryAddr": {
        "City": "Pedmont", 
        "Country": "USA", 
        "Line1": "456 n. 78 blvd", 
        "PostalCode": "45665", 
        "Lat": "40.1899498", 
        "Long": "-81.19959709999999", 
        "CountrySubDivisionCode": "OH", 
        "Id": "75"
    }, 
    "PrimaryPhone": {
        "FreeFormNumber": "(818) 555-1212"
    }, 
    "Active": true, 
    "ReleasedDate": "2014-02-01", 
    "MetaData": {
        "CreateTime": "2014-02-11T22:41:34-08:00", 
        "LastUpdatedTime": "2014-02-11T22:41:34-08:00"
    }, 
    "MiddleName": "For", 
    "Gender": "Male", 
    "HiredDate": "2011-02-04", 
    "BillRate": 654, 
    "SyncToken": "0", 
    "Suffix": "Dude", 
    "FamilyName": "You", 
    "SSN": "XXX-XX-XXXX", 
    "EmployeeNumber": "12Af", 
    "sparse": false, 
    "Id": "195"
}
"""
