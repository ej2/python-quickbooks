"""
This module is for API consumer-side filtering of QBOv3-querried transactions.
Many attributes cannot be used for filtering in QB, so the working solution
    is to pull down EVERYTHING and filter it here.

Actually, most of the filtering happens in the report module (see quick_report),
    but in order for that to happen, the data needs to be made manageable using
    some of the functions here...
"""

import json, pprint
from datetime import *
import reference as qbrefs

def invert_polarity(posting_type):
    if posting_type == "Credit":
        return "Debit"
    elif posting_type == "Debit":
        return "Credit"
    else:
        raise Exception("invert_polarity only takes 'Debit' or 'Credit'!")

def get_line_account(line_dict, qbbo, name=False):
    """different line dictionaries have different paths to the account for...
    ...apparently it depends on the object type"""

    if qbbo in ["JournalEntry"]:

        account_id        = line_dict["JournalEntryLineDetail"]\
                            ["AccountRef"]["value"]

        account_name      = line_dict["JournalEntryLineDetail"]\
                            ["AccountRef"]["name"]

    elif qbbo in ["Bill", "Purchase"]:

        account_id        = line_dict["AccountBasedExpenseLineDetail"]\
                            ["AccountRef"]["value"]              

        account_name      = line_dict["AccountBasedExpenseLineDetail"]\
                            ["AccountRef"]["name"]              

    else:
        pp = pprint.PrettyPrinter(indent=1)
        pp.pprint(line_dict)
        raise Exception("Tell me how to find the account in a %s object!" %\
                        qbbo)
    if name:
        return account_name
    else:
        return account_id

def find_by_name(qbbo_list, name, qbs):
    """
    Looks up an object by its name, returning that object's Id (if found)
     or else None if not.

    Will raise an exception if more than one is found -- this is a situation
     to avoid, for the judicious bookkeeper that might be reading this
     __doc__ string...
    """

    hit_list = []

    if isinstance(qbbo_list, (str, unicode)):

        qbbo_list = [qbbo_list]


    inspection_attr = {
        
        "Account" : "FullyQualifiedName",
        "Vendor"  : "DisplayName",
        "Customer": "FullyQualifiedName",
        "Employee": "DisplayName"

    }
    
    for qbbo in qbbo_list:

        name_key = inspection_attr[qbbo]

        for Id, o in qbs.get_objects(qbbo).iteritems():

            if o[name_key] == name:

                hit_list.append((qbbo,Id))

    if len(hit_list) == 0:

        return None, None

    elif len(hit_list) > 1:

        raise Exception("More than one thing is named %s: %s." \
                        % (name, hit_list))

    else:

        return hit_list[0]

def fabricate(qbbo, name, qbs):
    """
    This is really for creating Vendor and Customer objects on the fly.
    (Potentially we want to add Employees at a later date.)
    
    Generates a basic object with nothing but the name that's passed in,
     creates a json dict, creates the object, and returns the json dict.
    """

    #To Do: Be able to handle Jobs (not just top level customers)...
    #currently, a colon will pro'ly break this thing

    if qbbo in ["Vendor", "Customer"]:

        request_body = json.dumps({"DisplayName":name}, indent=4)

    else:
        
        raise NotImplementedError("Only Vendors and Customers for now...")

    return qbs.create_object(qbbo, request_body, "json")

def line_entity(line_dict, qbbo, name=False):
    """different line dictionaries have different paths to the Entity for...
    ...apparently it depends on the object type"""

    if qbbo in ["JournalEntry"]:
        Id         = line_dict["AccountBasedExpenseLineDetail"]\
                            ["Entity"]["EntityRef"]["value"]
        eneity_name       = line_dict["AccountBasedExpenseLineDetail"]\
                            ["Entity"]["EntityRef"]["name"]
    else:
        raise Exception("Tell me how to find the account in a %s object!" %\
                        qbbo)

    if name:
        return entity_name
    else:
        return Id
     
def entity_list(raw_entities_dict):
    """
    Returns a list of tuples that preserves the qbbo_types and Id keys.
    
    (The input is what you get when you run quickbooks.transactions()
     or quickbooks.names())

    Each item in list is a three-item tuple:
    (qbbo_type,Id,raw_entity_dict)
    """
    e_list = []

    for qbbo in raw_entities_dict:

        for Id in raw_entities_dict[qbbo]:
            
            raw_QBBO_dict = raw_entities_dict[qbbo][Id]

            e_list.append((qbbo, Id, raw_QBBO_dict))

    return e_list

def sure_id(qbo_session, qbbo, name_or_id, want = 'Id'):
    """Looks up the Id of an entity by it's name. Sometimes we'll want to
    take EITHER a name Or an Id (not knowing what the input will be) and return
    an Id, or maybe instead return a name. The 'want' paramter allows us to
    specify the output."""

    name_match = id_match = None

    entity_dict = qbo_session.get_objects(qbbo)

    for e_id in entity_dict:
        
        e_dict = entity_dict[e_id]
        if "FullyQualifiedName" in e_dict:
            e_name = e_dict["FullyQualifiedName"]
        else:
            e_name = e_dict["name"]

        if name_or_id == e_id:

            id_match = e_id

        if name_or_id == e_name:

            name_match = e_name

    #let's just account for a quick edge case here...
    if not name_match == None and not id_match == None and \
       not name_match == id_match:

        raise Exception("A different %s than Id %s has name %s!" % \
                        (qbbo, id_match, name_natch))


    if want in ["Id", "value"]:
        return id_match
    elif want in ["name"]:
        return name_match
    elif want in ["FullyQualifiedName","fqa"]:
        return 

def name_list(qbo_session, headers=True, debug=False):
    """
    Takes a packed name entity and returns something standardized.

    Initially, at least, this will only support these Business Objects:

     Customer
     Vendor
     Employee 

    Note that there is no intermediate method like what ledger_lines() uses
     in the ledgerize() method. First we create the name_list directly from the
     session. Then we set the session's name_list attribute and return it.
    """

    header_list = [              
        "qbbo", "Id", "domain", "SyncToken", "Active",
        "FamilyName", "Title", "GivenName",
        "MiddleName", "Suffix", "PrintOnCheckName", "DisplayName",
        "PrimaryEmailAddr", "PrimaryPhone", "Mobile",
        "billing_City", "billing_Country", "billing_Line1",
        "billing_PostalCode", "billing_Lat", "billing_Long",
        "billing_CountrySubDivisionCode", "billing_Id",
        "AlternatePhone", "Fax",
        "tax_id",
        "WebAddr", "CompanyName", "Balance",
        "PaymentMethodRef", "Notes", "PreferredDeliveryMethod",
        "shipping_City", "shipping_Country", "shipping_Line1",
        "shipping_PostalCode", "shipping_Lat", "shipping_Long",
        "shipping_CountrySubDivisionCode", "shipping_Id",
        "ResaleNum", "SalesTermRef", "FullyQualifiedName", "BillWithParent",
        "Job", "BalanceWithJobs", "Taxable", "Parent", "Level",
        "AcctNum", "Vendor1099",
        "Gender", "HiredDate", "ReleasedDate", "BillableTime", "BillRate",
        "EmployeeNumber"
    ]

    billing_address_key = {

        "Vendor"    : "BillAddr",
        "Customer"  : "BillAddr",
        "Employee"  : "PrimaryAddr"

    }

    tax_id_key = {

        "Vendor"   : "TaxIdentifier",
        "Employee" : "SSN"

    }

    name_lines = []

    if headers:

        name_lines.append(header_list)

    elif headers == "Only":

        return header_list

    if not hasattr(qbo_session,"names_list"):

        #do the sifting...fun; we can go in order of object type because
        #that's how the sessions object_dicts are organized (from the query)
        
        vce_names = qbo_session.object_dicts(["Vendor", "Customer", "Employee"])
        vce_list  = entity_list(vce_names)

        for name_dict in vce_list:

            name_list_line = []

            qbbo, Id, rod = name_dict   #(rod = raw object dictionary)

            for h in header_list:

                if h == "qbbo":

                    name_list_line.append(qbbo)
                
                elif h in rod:

                    if h in ["PrimaryPhone", "AlternatePhone", "Mobile", "Fax"]:

                        name_list_line.append(rod[h]["FreeFormNumber"])

                    elif h in ["PrimaryEmailAddr"]:

                        name_list_line.append(rod[h]["Address"])

                    elif h in ["WebAddr"]:

                        name_list_line.append(rod[h]["URI"])

                    elif h in ["SalesTermRef",
                               "PaymentMethodRef",
                               "TermRef",
                               "ParentRef"]:

                        name_list_line.append(rod[h]["value"])

                    else:

                        name_list_line.append(rod[h])                        

                elif h[:8] == "billing_" or h[:9] == "shipping_":

                    if h[:8] == 'billing_':

                        addy_key = billing_address_key[qbbo]

                    else:

                        addy_key = "ShipAddr"

                    addy_bit = h.split("_",1)[1]

                    if addy_key in rod and addy_bit in rod[addy_key]:
                        
                        name_list_line.append(rod[addy_key][addy_bit])
                    
                    else:
                    
                        name_list_line.append(None)                   

                elif h == "tax_id":

                    #be careful with this, because for employees, the API
                    #returns just XXX-XX-XXXX no matter what...don't overwrite
                    #any actual date (which you probably shouldn't be storing
                    #anyway, so there)

                    if qbbo == "Customer":

                        name_list_line.append(None)

                    else:

                        k = tax_id_key[qbbo]

                        if k in rod:

                            name_list_line.append(rod[k])

                        else:

                            name_list_line.append(None)

                else:

                    #raise Exception("How to handle the %s?" % h)
                    name_list_line.append(None)

            name_lines.append(name_list_line)

        #sort the whole list alphabetically (later perhaps offering options)

        qbo_session.names_list = name_lines

    return qbo_session.names_list


def ledgerize(transaction, qbo_session=None, headers=False, debug=False):
    """
    Takes a packed transaction entity (BillPayment, Purchase,
    etc., as represented by a single element in the dictionary returned
    by entity_dict()), and returns a tabular data structure that identifies the
    transaction, much like a set of general ledger lines.

    Where capital letters are used in variable names, it's generally
    to indicate that it's the case-faithful QuickBooks business object
    property name...sorry I'm breaking the naming conventions, but
    I think it's worth it to avoid confusion here.

    If a quickbooks.qbo_session is passed, it's namelists will be used to look
    up any cross-referenced transactions (such as an item's associate account),
    otherwise some placeholder will be used...
    """

    ledger_lines = []

    #is it a problem that I'm excluding "Adjustment"?

    header_list = [  
            
        "company_id", "qbbo", "Id", "line_number",
        "domain", "entry_subtype", "SyncToken",
        "DocNumber", "TxnDate", "CreateTime", "LastUpdatedTime",
        "PrivateNote",
        "line_account", "CurrencyRef", "Amount",
        "Description", "EntityRef",
        "DepartmentRef", "ClassRef",
        "LinkedTxn"

    ]


    if headers:

        return header_list

    amount_i = header_list.index("Amount")

    #first, unpack the tuple: rod -- raw_object_dictionary

    qbbo, Id, rod = transaction

    if debug:
        print qbbo, Id

    #now, we start with the header and move to the lines...

    #first let's set the common header properties (required then optional)

    company_id               = qbo_session.company_id
    Id                       = rod["Id"]
    TxnDate                  = datetime.strptime(rod["TxnDate"], "%Y-%m-%d")
    CreateTime               = rod["MetaData"]["CreateTime"] 
    LastUpdatedTime          = rod["MetaData"]["LastUpdatedTime"] 
    SyncToken                = rod["SyncToken"]
    domain                   = rod["domain"]
    Description              = ""    #unless it's a JE, I THINK...
    DepartmentRef          = "Not implemented yet!"
    ClassRef               = "Not implemented yet!"
    

    if "CurrencyRef" in rod:
        CurrencyRef          = rod["CurrencyRef"]["value"]
    else:
        CurrencyRef          = ""

    if "PrivateNote" in rod:
        PrivateNote     = rod["PrivateNote"]
    else:
        PrivateNote     = ""

    if "DocNumber" in rod:
        DocNumber          = rod["DocNumber"]
    else:
        DocNumber          = ""

    if "Adjustment" in rod:
        Adjustment           = rod["Adjustment"]
    else:
        Adjustment           = ""

    if "LinkedTxn" in rod:

        LinkedTxn  = []

        for lt in rod["LinkedTxn"]:
            lt_doc           = lt["TxnType"]
            lt_num           = lt["TxnId"]
            LinkedTxn.append(lt_doc+"/"+lt_num)

        LinkedTxn  = "; ".join(LinkedTxn)

    else:

        LinkedTxn  = ""

    if "TotalAmt" in rod:
        TotalAmt             = rod["TotalAmt"]
    #else, it's a JournalEntry and has no TotalAmt...

    #now let's deal with properties unique to certain objects

    if qbbo == "Bill":

        entry_subtype = "Bill"
        #head_account  = rod["APAccountRef"]["name"]
        """

        https://developer.intuit.com/docs/0025_quickbooksapi/
            0050_data_services/030_entity_services_reference/bill

        it's possible to rename and/or have more than
        one AP account, but because BillPayment objects don't show
        account information at the split level, it's probably a look-up
        operation (to the linked transaction) to figure it out.
        Hence, we're going the easy route and assuming the thing is just
        called "Accounts Payable."

        Then again, it appears the QBO doesn't even support using the
        Bill feature to switch from the default Accounts Payable, per:

        https://community.intuit.com/questions/780986-assign-an-accounts
            -payable-account-to-a-bill-in-quickbooks-online
        """
        head_account     = "Accounts Payable"
        EntityRef             = rod["VendorRef"]["name"]
        polarity         = "Credit"

    elif qbbo == "BillPayment":

        entry_subtype    = rod["PayType"]

        #Some "BillPayments" just represent "applying a payment,"
        #where a check or other item is matched to an oustanding
        #bill. In this case, whatever entry is so matched ALREADY
        #must have debited accounts payable, so we're going to just
        #keep this entry for the transaction linkages (important!)
        #We'll be debiting AND crediting A/P in the same entry...

        if "BankAccountRef" not in rod["CheckPayment"]:
            head_account = "Accounts Payable"
        else:
            head_account = rod["CheckPayment"]\
                           ["BankAccountRef"]["name"]
        EntityRef             = rod["VendorRef"]["name"]
        polarity         = "Credit"

        #TODO: Is there an UnappliedAmt like there is with Payment objects?

    elif qbbo == "Invoice":

        entry_subtype    = "Invoice"
        #account isn't explicitly stated, so...
        head_account     = "Accounts Receivable"
        EntityRef             = rod["CustomerRef"]["name"]
        polarity         = "Debit"    

    elif qbbo == "JournalEntry":

        entry_subtype    = "JournalEntry"

    elif qbbo == "Payment":

        entry_subtype    = "Payment"
        dep_account_id   = rod["DepositToAccountRef"]["value"]
        head_acct_dict   = qbo_session.get_entity("Account", dep_account_id)
        head_account     = head_acct_dict["FullyQualifiedName"]
        polarity         = "Debit"                    #to cash / asset acct
        customer_id      = rod["CustomerRef"]["value"]
        name_dict        = qbo_session.get_entity("Customer", customer_id)
        EntityRef             = name_dict["FullyQualifiedName"]
        
        #I have a feeling the unapplied amount is going to be a problem
        #but we'll have to cross that bridge when we come to it...
        UnappliedAmt     = rod["UnappliedAmt"]

        if "PaymentRefNum" in rod:
            document_number  = rod["PaymentRefNum"]

        else:
            document_number  = ""

    elif qbbo == "Purchase":

        entry_subtype    = rod["PaymentType"]
        head_account     = rod["AccountRef"]["name"]

        #CC charges, e.g., don't have to have a name...

        if "EntityRef" not in rod:
            EntityRef         = ""
        else:
            EntityRef         = rod["EntityRef"]["name"]

        if "Credit" in rod and rod["Credit"] == "True":

            #QB uses credit in the customer-centric sense, i.e. "yay, I get
            # a credit!" This is the opposit of crediting the cash account,
            # but hey, that's the way Intuit went with this

            polarity         = "Debit"  #yes, counterintuitive

        else:

            polarity         = "Credit"   #such as a Credit Card Credit

    else:

        raise NotImplementedError("Implement QuickBooks.ledgerize()"+\
                                  " for %s objects!" % qbbo, "e.g:",\
                                  "%s" % Id)

    #JournalEntries, uniquely, have no 'header', so their first line
    #(which QB labels with Id=0) is the the first 'Line'
    #for all other object types though:

    if not qbbo in ["JournalEntry"]:

        #QB shows all amounts as positive (like many GL systems)
        #For simplicity, it's sometimes easier to have credits simply
        #appear as negative numbers, so we're flipping the sign of the
        #amounts as necessary....        

        if polarity == "Credit":
            Amount = -TotalAmt
        else:
            Amount = TotalAmt

        line_number = 0

        ledger_lines.append([
        
            company_id, qbbo, Id, line_number,
            domain, entry_subtype, SyncToken,
            DocNumber, TxnDate, CreateTime, LastUpdatedTime,
            PrivateNote,
            head_account, CurrencyRef, Amount,
            Description, EntityRef,
            DepartmentRef, ClassRef,
            LinkedTxn
       
        ])

        """
        old list...
        
        TxnDate, qbbo, Id, 0, entry_subtype,  #zero-indexed!
        domain, DocNumber,
        CreateTime, LastUpdatedTime, SyncToken, Adjustment,
        head_account, CurrencyRef, Amount,
        PrivateNote, EntityRef, DepartmentRef, ClassRef,
        joined_linked_transactions
        """

    #because at least one object type doesn't include line Ids,
    #we have to count the lines

    this_line_number = 0

    if len(rod["Line"])<1:

        #TODO -- FABRICATE A LINE

        """An example of where you need this is an unlinked BillPayment"""
        """It still hits A/P even if it has no line that links to a Bill"""
        """Same is true for unapplied Payments (for A/R)"""
        
        line_number                = 1
        Amount                     = -Amount

        #other attributes can be preserved from the header, e.g. EntityRef

        if qbbo == "BillPayment":
        
            line_account                = "Accounts Payable"
            Description            = "Unapplied BillPayment!"


        elif qbbo == "Payment":

            line_account                = "Accounts Receiveable"
            Description            = "Unapplied Receipt!"

        else:

            raise Exception("What should ledgerize do with a %s" % qbbo,\
                            " that has no split lines?") 

        ledger_lines.append([

            company_id, qbbo, Id, line_number,
            domain, entry_subtype, SyncToken,
            DocNumber, TxnDate, CreateTime, LastUpdatedTime,
            PrivateNote,
            line_account, CurrencyRef, Amount,
            Description, EntityRef,
            DepartmentRef, ClassRef,
            LinkedTxn

        ])

        """
        old list


        TxnDate, qbbo, Id, line_number, entry_subtype,
        domain, DocNumber,
        CreateTime, LastUpdatedTime, SyncToken, Adjustment,
        line_account, CurrencyRef, Amount,
        PrivateNote, Description, EntityRef,
        DepartmentRef, ClassRef,
        joined_linked_transactions

        """

    for split_line in rod["Line"]:

        DepartmentRef          = "Not implemented yet!"
        ClassRef               = "Not implemented yet!"

        this_line_number+=1

        #first the common properties, again
        try:
            Amount                   = split_line['Amount']
        except:
            #this must be a type of line OTHER than one hitting a financial
            #account, so let's skip it
            this_line_number-=1
            continue

        if "Id" in split_line:
            line_number          = split_line["Id"]
        else:
            line_number          = str(this_line_number)

        if "Description" not in split_line:
            Description      = ""
        else:
            Description      = split_line["Description"]

        if "LinkedTxn" in split_line:

            line_LinkedTxn = []

            for lt in split_line["LinkedTxn"]:
                
                lt_doc           = lt["TxnType"]
                lt_num           = lt["TxnId"]
                try:
                    lt_qbbo      = qbrefs.linked_txn_correction \
                                   [lt_doc]
                except KeyError:
                    print "Add %s to reference.linked_txn_correction!" %\
                        lt_doc, "For now, just using that name."
                    
                    lt_qbbo = lt_doc

                    #quit()
                            
                line_LinkedTxn.append(lt_qbbo+"/"+lt_num)

            line_LinkedTxn  = "; ".join(line_LinkedTxn)

        else:

            line_LinkedTxn = ""

        #add class!

        #now on to object-specific properties

        if qbbo == "Bill":

            line_account  = get_line_account(split_line, "Bill", name=True)
  
            polarity             = "Debit"

        elif qbbo == "BillPayment":

            #AP, per above, is kind of a special case
            line_account              = "Accounts Payable"

            #Every split line of a BillPayment should have a linked
            #transaction. The BillPayment line should have the OPPOSITE
            #polarity of the line in the transaction to which it's linked
            #THIS COULD BE A MISTAKE, BUT we're assuming that a BillPayment
            #line can only have ONE linked transaction...

            if lt_qbbo   == "Bill":

                polarity = "Debit"         #because bills always CREDIT A/P

            elif lt_qbbo == "Deposit":
                
                #THIS COULD DEFINITELY BE WRONG
                polarity = "Debit"

            elif lt_qbbo in ["JournalEntry", "Purchase"]:

                #now, of what polarity is the net entry to A/P in the JE?
                #we're assuming the header is of no relevance, because only
                #bills (of what's been implemented) have a header that touches 
                #A/P

                je_dict = qbo_session.get_entity(lt_qbbo, lt_num)

                net_ap_impact = 0

                for line in je_dict["Line"]:
                    line_amount      = line["Amount"]
                    line_account_id  = get_line_account(line, lt_qbbo)
                    
                    if line_account_id == qbo_session.get_ap_account():
                    
                        if lt_qbbo in ["JournalEntry"]:
                            line_polarity = line["JournalEntryLineDetail"]\
                                            ["PostingType"]

                        elif lt_qbbo in ["Purchase"]:

                            if "Credit" in je_dict and \
                               je_dict["Credit"] == "False":
                               
                                #again, x-intuitivetely (from the accounting
                                # standpoint, this means the header is
                                # a Credit, so the linked line is a Debit,
                                # so the reversal must be a Credit

                                line_polarity = "Credit"
                            else:
                                line_polarity = "Debit"
                        
                        else:
                            raise Exception("How can line_polarity == %s!?" %\
                                            line_polarity)

                        if line_polarity == "Credit":
                            net_ap_impact-=line_amount
                        elif line_polarity == "Debit":
                            net_ap_impact+=line_amount
                            
                        """
                        print split_line
                        print line
                        print "net_ap_impact:", net_ap_impact
                        """

                #ok, now let's invert the net A/P polarity of the linked_txn
                if net_ap_impact<=0:
                    polarity = "Debit"
                else:
                    polarity = "Credit"

            else:
                print split_line
                raise Exception("BillPayment %s is linked to a %s." %\
                                (Id, lt_doc), "What do I do?")

        elif qbbo == "Invoice":

            #we only want SalesItemLineDetail split_lines
            if not split_line["DetailType"] == "SalesItemLineDetail":
                continue

            item                 = split_line["SalesItemLineDetail"]\
                                   ["ItemRef"]["name"]

            if qbo_session == None:
              
                line_account          = "Look up account for Item %s!" % item
            
            else:
            
                item_id          = split_line["SalesItemLineDetail"]\
                                   ["ItemRef"]["value"]

                Items            = qbo_session.get_objects("Item")

                #print "Looking for account in Item[%s]." % item_id
                account_id       = Items[item_id]["IncomeAccountRef"]\
                                       ["value"]

                account_object   = qbo_session.get_objects("Account")\
                                   [account_id]

                line_account          = account_object["FullyQualifiedName"]

            polarity             = "Credit"

        elif qbbo == "JournalEntry":

            je_deets             = split_line["JournalEntryLineDetail"]

            line_account              = je_deets["AccountRef"]["name"]
            if "Entity" in je_deets:
                EntityRef             = je_deets["Entity"]["EntityRef"]["name"]
            else:
                EntityRef             = ""

            polarity             = je_deets["PostingType"]

        elif qbbo == "Payment":

            #I believe it ALWAYS has to be...
            line_account = "Accounts Receivable"
            polarity = "Credit"

        elif qbbo == "Purchase":

            line_account = split_line["AccountBasedExpenseLineDetail"]\
                      ["AccountRef"]["name"]
            polarity             = "Debit"

        else:
            print "This is an object type the method doesn't know."
            print "However, the script should never have made it here."

        if polarity == "Credit":
            Amount = -Amount
        else:
            Amount = Amount

        ledger_lines.append([

            company_id, qbbo, Id, line_number,
            domain, entry_subtype, SyncToken,
            DocNumber, TxnDate, CreateTime, LastUpdatedTime,
            PrivateNote,
            line_account, CurrencyRef, Amount,
            Description, EntityRef,
            DepartmentRef, ClassRef,
            LinkedTxn

        ])

        """
        old list

        TxnDate, qbbo, Id, line_number, entry_subtype,
        domain, DocNumber,
        CreateTime, LastUpdatedTime, SyncToken, Adjustment,
        line_account, CurrencyRef, Amount,
        PrivateNote, Description, EntityRef,
        joined_line_linked_transactions
        
        """


    #quickly validate the JE to make sure that it at least totals to zero!

    check_sum = 0

    for line in ledger_lines:
        check_sum = round(check_sum + line[amount_i],2)

    if not check_sum == 0:
        print"ledger_lines of %s %s don't total to zero!" % \
                        (qbbo, Id)

    return ledger_lines

def ledger_lines(qbo_session,
                 qbbo=None,
                 Id=None,
                 line_number=None,
                 headers=False,
                 **kwargs):
    """
    For efficiency, it's often helpful to ledgerize every transaction
     and just look them up by qbbo, id, and line_number.

    If ALL lines are called and that operation hasn't already been done, it will
     get done once and then subsequently use the existing dictionary to call
     look up the line by reference). Call all the lines by leaving the optional
     arguments at their defaults (None).

    Of course, it's also possible to get a subset of lines, and for that we use
     a different mechanism. Call that using the parameters.
    """

    ledger_lines_list = []
    header_list       = qbo_session.ledgerize("_", headers=True)

    if headers:

        ledger_lines_list = [header_list]

    if qbbo == None and Id == None and line_number == None:

        if not hasattr(qbo_session, "ledger_lines_dict"):

            if 'query_tail' in kwargs:
                qt = kwargs['query_tail']
            else:
                #qt = "WHERE MetaData.LastUpdatedTime >= '2014-02-04'"
                qt = ""

            transactions = entity_list(qbo_session.transactions(
                requery=False, params = {}, query_tail = qt))
            
            qbo_session.ledger_lines = []

            ledger_lines_dict = {}

            #where in the headesr is "line_number"?
            line_i = header_list.index("line_number")

            for t in transactions:

                qbbo, Id, _ = t

                this_transactions_lines = qbo_session.ledgerize(t)

                for line in this_transactions_lines:

                    k = qbbo+Id+str(line[line_i])

                    ledger_lines_dict[k] = line

            #let's first sort by date...for good measure
            #date is the first element in the ledgerize output (for now)
            date_ordered_k_list = sorted(ledger_lines_dict.iterkeys(), key= \
                                         lambda k: ledger_lines_dict[k][0])

            if len(date_ordered_k_list)<1:
                return []

            first_transaction      = ledger_lines_dict[date_ordered_k_list[0]]
            last_transaction      = ledger_lines_dict[date_ordered_k_list[-1]]
            
            #these dates will streamline reporting (see e.g. report.pnl)

            qbo_session.first_date = first_transaction[0]
            qbo_session.last_date  = first_transaction[0]

            for k in date_ordered_k_list:
                qbo_session.ledger_lines.append(ledger_lines_dict[k])

        else:
            #TODO: build in a requery for when the company file is adjusted
            pass

        ledger_lines_list+=qbo_session.ledger_lines

    else:
        
        raw_transactions      = qbo_session.object_dicts(qbbo)[qbbo]

        if not Id == None:

            if qbbo == None:
                raise Exception("Can't give an Id (%s) and no object type." % \
                                Id)
            
            transactions = [(qbbo, Id, raw_transactions[Id])]

        else:

            transactions = entity_list(raw_transactions)
        
        for t in transactions:

            t_ledger_lines = ledgerize(t, qbo_session)

            if line_number == None:

                if qbbo == None or Id == None:
                    raise Exception("Can't give a line_number (%s)" % \
                                    line_number, "and not also a qbbo and",
                                    "an Id.")

                ledger_lines_list+=t_ledger_lines

            else:
                
                ledger_lines_list.append(t_ledger_lines[line_number])
            
    return ledger_lines_list 

import collections

ledger_line_fields = [
    'company_id', 'qbbo', 'Id', 'line_number',
    'domain', 'entry_subtype', 'SyncToken',
    'DocNumber', 'TxnDate', 'CreateTime', 'LastUpdatedTime',
    'PrivateNote',
    'line_account', 'CurrencyRef', 'Amount',
    'Description', 'EntityRef',
    'DepartmentRef', 'ClassRef',
    'LinkedTxn'
]

ledger_line = collections.namedtuple("ledger_line", ledger_line_fields)

def qbboify(raw_ledger_line_list, qbs, auto_create_vcs = True):
    """
    Does the opposite of ledgerize. The output should be something that
     can be uploaded as a qbbo (for a create, update, or delete operation).

    If the ledger_lines come WITH an entry_ID, we'll use it (as it's probably
     for an update or a delete). If there's NO sync token, we'll need to read
     the object in first in order to get the sync token. If there IS a sync
     token, we'll assume that it's correct and if not we'll throw an exception.

    NOTE: the input for this is a list of lists. Each list becomes a named
     tuple here.

    As you might expect, you DO need a Quickbooks session to do cross-
     referencing of names, accounts, and transaction linkages, etc.

    TO DO: WHERE ARE THE ATTACHMENTS? SEE jlrww JournalEntry 1069, which HAS
     an attachment that doesn't appear to be showing up when the entry is
     querried. (Maybe it WILL show up in a read?)

    Auto_create_vcs will create new Vendor and Customer objects for names that
     don't already exist in the QBO company. Can save time. (This isn't
     available for Account objects mostly because it strikes me as a bad idea.)
    """

    q_dict = {}
    
    lls = []                                #there should be AT LEAST two...

    for raw_ll in raw_ledger_line_list:

        lls.append(ledger_line._make(raw_ll))

    qbbo = lls[0].qbbo
    
    if qbbo == "JournalEntry":
      
        #mandatory, then optional ENTRY-level attributes
        
        q_dict['sparse']      = False
        q_dict['CurrencyRef'] = {"name" :"United States Dollar",
                                 "value":"USD"}
        q_dict['domain']      = "QBO"

        q_dict['TxnDate'] = "%s" % getattr(lls[0], "TxnDate").date()

        for attr in ['PrivateNote', 'SyncToken',
                     'DocNumber', 'Adjustment', 'Id']:
            
            if hasattr(lls[0], attr):
            
                val = getattr(lls[0], attr)

                if not val == None:

                    q_dict[attr] = val

        #now let's do the same for each LINE of the JE

        line_dict_list = []

        for ll in lls:

            #again, mandatory then optional

            line_dict = {"DetailType":"JournalEntryLineDetail"}

            line_dict["Id"] = ll.line_number

            for attr in ["Description"]:

                val = getattr(ll, attr)

                if not val == None:

                    line_dict[attr] = val

            #and now we go a level DEEPER!

            if ll.Amount >= 0:
                polarity = "Debit"
            else:
                polarity = "Credit"

            line_dict['Amount'] = round(abs(float(ll.Amount)),2)

            detail_dict = {"PostingType":polarity}
            
            #We need the Id, but the user shouldn't need it
            #So we'll look it up in the session dict

            _, account_id = find_by_name("Account", ll.line_account, qbs)

            if account_id == None:

                raise Exception("%s is not an existing account" \
                                % ll.line_account)

            detail_dict['AccountRef'] = {"name":ll.line_account,
                                         "value"  :account_id}

            if not ll.EntityRef == None:

                entity_name = ll.EntityRef

                #we allow this option to enumerate the entity_type
                if "|||" in entity_name:

                    entity_name, entity_type = entity_name.split("|||") 


                qbbo_list = ["Customer", "Vendor", "Employee"]

                entity_type, entity_id = find_by_name(qbbo_list,
                                                      entity_name,
                                                      qbs)

                if entity_id == None:

                    if not auto_create_vcs:

                        error_message = "No Customer, Vendor, or "+\
                                        "Employee called %s exists." \
                                        % ll.EntityRef

                        raise Exception(error_message)

                    else:

                        #create a customer if the line is an income account...
                        #otherwise create a vendor
                        
                        #yes, better to guess than slow the process down every
                        #time a new name comes along

                        account_classification = qbs.get_objects("Account")\
                                                 [account_id]["Classification"]

                        if not entity_type == None:

                            pass
                            
                        elif account_classification == "Revenue":

                            entity_type = "Customer"

                        else:

                            entity_type = "Vendor"

                        new_entity_dict = fabricate(entity_type,
                                                    entity_name,
                                                    qbs)

                        entity_id   = new_entity_dict["Id"]
                            
                detail_dict["Entity"] = {"Type":entity_type,
                                         "EntityRef":
                                         {"name":entity_name,
                                          "value"  :entity_id}}
                
            if not ll.DepartmentRef == None:

                dept_id = find_by_name("Department", ll.DepartmentRef)

                detail_dict["DepartmentRef"] = {"name":ll.Department,
                                                "value"  :dept_id}

            if not ll.ClassRef == None:

                class_id = find_by_name("Class", ll.ClassRef)

                detail_dict["ClassRef"] = {"name":ll.Department,
                                           "value"  :class_id}

            line_dict["JournalEntryLineDetail"] = detail_dict

            line_dict_list.append(line_dict)

        q_dict["Line"] = line_dict_list

    else:
        
        raise Exception("%s\nDon't know how to create this type of object." \
                        % lls)

    return qbbo, json.dumps(q_dict, indent=4), "json"
