"""
This module is for API consumer-side filtering of QBOv3-querried transactions.
Many attributes cannot be used for filtering in QB, so the working solution
    is to pull down EVERYTHING and filter it here.
"""

import pprint
import reference as qbrefs

def invert_polarity(posting_type):
    if posting_type == "Credit":
        return "Debit"
    elif posting_type == "Debit":
        return "Credit"
    else:
        raise Exception("invert_polarity only takes 'Debit' or 'Credit'!")

def line_account(line_dict, qbbo, name=False):
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

def line_entity(line_dict, qbbo, name=False):
    """different line dictionaries have different paths to the Entity for...
    ...apparently it depends on the object type"""

    if qbbo in ["JournalEntry"]:
        entity_id         = line_dict["AccountBasedExpenseLineDetail"]\
                            ["Entity"]["EntityRef"]["value"]
        eneity_name       = line_dict["AccountBasedExpenseLineDetail"]\
                            ["Entity"]["EntityRef"]["name"]
    else:
        raise Exception("Tell me how to find the account in a %s object!" %\
                        qbbo)

    if name:
        return entity_name
    else:
        return entity_id
     
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

    if headers:

        headers = [              
            "TxnDate", "qbbo_type", "entity_id", 
            "line_number", "document_type",
            "domain", "user_number",
            "CreateTime", "LastUpdatedTime", "SyncToken", "Adjustment",
            "account", "amount", "description", "name",
            "linked_transactions"
        ]

        return headers

    #first, unpack the tuple: rod -- raw_object_dictionary

    qbbo, Id, rod = transaction

    if debug:
        print qbbo, Id

    #now, we start with the header and move to the lines...

    #first let's set the common header properties (required then optional)

    entity_id                = rod["Id"]
    TxnDate                  = rod["TxnDate"]
    CreateTime               = rod["MetaData"]["CreateTime"] 
    LastUpdatedTime          = rod["MetaData"]["LastUpdatedTime"] 
    SyncToken                = rod["SyncToken"]
    domain                   = rod["domain"]
    #add department!

    if "PrivateNote" in rod:
        head_description     = rod["PrivateNote"]
    else:
        head_description     = ""

    if "DocNumber" in rod:
        user_number          = rod["DocNumber"]
    else:
        user_number          = ""

    if "Adjustment" in rod:
        Adjustment           = rod["Adjustment"]
    else:
        Adjustment           = ""

    linked_transactions  = []
    joined_linked_transactions  = ""

    if "LinkedTxn" in rod:

        for lt in rod["LinkedTxn"]:
            lt_doc           = lt["TxnType"]
            lt_num           = lt["TxnId"]
            linked_transactions.append(lt_doc+"/"+lt_num)

        joined_linked_transactions  = "; ".join(linked_transactions)


    if "TotalAmt" in rod:
        TotalAmt             = rod["TotalAmt"]
    #else, it's a JournalEntry and has no TotalAmt...

    #now let's deal with properties unique to certain objects

    if qbbo == "Bill":

        document_type = "Bill"
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
        name             = rod["VendorRef"]["name"]
        polarity         = "Credit"

    elif qbbo == "BillPayment":

        document_type    = rod["PayType"]

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
        name             = rod["VendorRef"]["name"]
        polarity         = "Credit"

        #TODO: Is there an UnappliedAmt like there is with Payment objects?

    elif qbbo == "Invoice":

        document_type    = "Invoice"
        #account isn't explicitly stated, so...
        head_account     = "Accounts Receivable"
        name             = rod["CustomerRef"]["name"]
        polarity         = "Debit"    

    elif qbbo == "JournalEntry":

        document_type    = "JournalEntry"

    elif qbbo == "Payment":

        document_type    = "Payment"
        dep_account_id   = rod["DepositToAccountRef"]["value"]
        head_acct_dict   = qbo_session.get_entity("Account", dep_account_id)
        head_account     = head_acct_dict["FullyQualifiedName"]
        polarity         = "Debit"                    #to cash / asset acct
        customer_id      = rod["CustomerRef"]["value"]
        name_dict        = qbo_session.get_entity("Customer", customer_id)
        name             = name_dict["FullyQualifiedName"]
        document_number  = rod["PaymentRefNum"]
        
        #I have a feeling the unapplied amount is going to be a problem
        #but we'll have to cross that bridge when we come to it...
        UnappliedAmt     = rod["UnappliedAmt"]

    elif qbbo == "Purchase":

        document_type    = rod["PaymentType"]
        head_account     = rod["AccountRef"]["name"]

        #CC charges, e.g., don't have to have a name...

        if "EntityRef" not in rod:
            name         = ""
        else:
            name         = rod["EntityRef"]["name"]

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
            amount = -TotalAmt
        else:
            amount = TotalAmt

        ledger_lines.append([
            TxnDate, qbbo, entity_id, 0, document_type,  #zero-indexed!
            domain, user_number,
            CreateTime, LastUpdatedTime, SyncToken, Adjustment,
            head_account, amount, head_description, name,
            joined_linked_transactions
        ])

    #because at least one object type doesn't include line Ids,
    #we have to count the lines

    this_line_number = 0

    if len(rod["Line"])<1:
        #TODO -- FABRICATE A LINE
        """An example of where you need this is an unlinked BillPayment"""
        """It still hits A/P even if it has no line that links to a Bill"""
        """Same is true for unapplied Payments (for A/R)"""
        
        line_number                = 1
        amount                     = -amount

        #other attributes can be preserved from the header, e.g. name

        if qbbo == "BillPayment":
        
            account                = "Accounts Payable"
            Description            = "Unapplied BillPayment!"


        elif qbbo == "Payment":

            account                = "Accounts Receiveable"
            Description            = "Unapplied Receipt!"

        else:

            raise Exception("What should ledgerize do with a %s" % qbbo,\
                            " that has no split lines?") 

        ledger_lines.append([
            TxnDate, qbbo, entity_id, line_number, document_type,
            domain, user_number,
            CreateTime, LastUpdatedTime, SyncToken, Adjustment,
            account, amount, Description, name,
            joined_linked_transactions
        ])

    for split_line in rod["Line"]:

        this_line_number+=1

        #first the common properties, again
        Amount                   = split_line['Amount']

        if "Id" in split_line:
            line_number          = split_line["Id"]
        else:
            line_number          = str(this_line_number)

        if "Description" not in split_line:
            Description      = ""
        else:
            Description      = split_line["Description"]

        line_linked_transactions = []
        joined_line_linked_transactions  = ""

        if "LinkedTxn" in split_line:

            for lt in split_line["LinkedTxn"]:
                
                lt_doc           = lt["TxnType"]
                lt_num           = lt["TxnId"]
                try:
                    lt_qbbo      = qbrefs.linked_txn_correction \
                                   [lt_doc]
                except KeyError:
                    print "Add %s to reference.linked_txn_correction!" %\
                        lt_doc
                    quit()
                            
                line_linked_transactions.append(lt_qbbo+"/"+lt_num)

            joined_line_linked_transactions  = "; ".join(
                line_linked_transactions
            )

        #add class!

        #now on to object-specific properties

        if qbbo == "Bill":

            account  = line_account(split_line, "Bill", name=True)
  
            polarity             = "Debit"

        elif qbbo == "BillPayment":

            #AP, per above, is kind of a special case
            account              = "Accounts Payable"

            #Every split line of a BillPayment should have a linked
            #transaction. The BillPayment line should have the OPPOSITE
            #polarity of the line in the transaction to which it's linked
            #THIS COULD BE A MISTAKE, BUT we're assuming that a BillPayment
            #line can only have ONE linked transaction...

            if lt_qbbo   == "Bill":

                polarity = "Debit"         #because bills always CREDIT A/P

            elif lt_qbbo in ["JournalEntry", "Purchase"]:

                #now, of what polarity is the net entry to A/P in the JE?
                #we're assuming the header is of no relevance, because only
                #bills (of what's been implemented) have a header that touches 
                #A/P

                je_dict = qbo_session.get_entity(lt_qbbo, lt_num)

                net_ap_impact = 0

                for line in je_dict["Line"]:
                    line_amount      = line["Amount"]
                    line_account_id  = line_account(line, lt_qbbo)
                    
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
              
                account          = "Look up account for Item %s!" % item
            
            else:
            
                item_id          = split_line["SalesItemLineDetail"]\
                                   ["ItemRef"]["value"]

                Items            = qbo_session.get_objects("Item")

                #print "Looking for account in Item[%s]." % item_id
                account_id       = Items[item_id]["IncomeAccountRef"]\
                                       ["value"]

                account_object   = qbo_session.get_objects("Account")\
                                   [account_id]

                account          = account_object["FullyQualifiedName"]

            polarity             = "Credit"

        elif qbbo == "JournalEntry":

            je_deets             = split_line["JournalEntryLineDetail"]

            account              = je_deets["AccountRef"]["name"]
            if "Entity" in je_deets:
                name             = je_deets["Entity"]["EntityRef"]["name"]
            else:
                name             = ""

            polarity             = je_deets["PostingType"]

        elif qbbo == "Payment":

            #I believe it ALWAYS has to be...
            account = "Accounts Receivable"
            polarity = "Credit"

        elif qbbo == "Purchase":

            account = split_line["AccountBasedExpenseLineDetail"]\
                      ["AccountRef"]["name"]
            polarity             = "Debit"

        else:
            print "This is an object type the method doesn't know."
            print "However, the script should never have made it here."

        if polarity == "Credit":
            amount = -Amount
        else:
            amount = Amount

        ledger_lines.append([
            TxnDate, qbbo, entity_id, line_number, document_type,
            domain, user_number,
            CreateTime, LastUpdatedTime, SyncToken, Adjustment,
            account, amount, Description, name,
            joined_line_linked_transactions
        ])


    #quickly validate the JE to make sure that it at least totals to zero!

    check_sum = 0

    for line in ledger_lines:
        #print line[11]
        check_sum = round(check_sum + line[12],2)

    if not check_sum == 0:
        print"ledger_lines of %s %s don't total to zero!" % \
                        (qbbo, Id)

    return ledger_lines
