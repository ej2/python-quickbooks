"""
This module is for API consumer-side reporting on QBOv3-querried transactions.
 In addition to mimmicking such features as "QuickReport," "General Ledger,"
 "Profit & Loss," et al, it provides some helpful functions, such as finding
 the starting and ending balance of a particular account as of a particular
 date and, of course, finding the total activity between two dates.
"""

import reference as qbrefs
import massage   as qbm
import copy

def quick_report(qbo_session, filter_attributes={}, headers=True):
    """
    Simulates a 'Quick Report' in QB by pulling getting the lines of
    all transactions that match the attributes we're passed.

    This match is a simple eq (=) matcher because that's how QB does it
    as a first cut. You can later filter by date, total by various things,
    etc., but this doesn't do that...other reporting tools will.

    One potentially helpful tool though is the ability to include multiple
    criteria for any one attribute (in the form of a list), so you can
    run a quick_report on several classes and several accounts at once, e.g.

    Note that even though QB can do a "Quick Report" on a vendor
    or other Name List-type object, this method can't (yet). This is for
    transactions ONLY.

    Also note that because a quick_report pulls in PARTIAL transactions,
    we aren't going to return  whole transactions. Rather, we're going
    to return ledger-like lines of relevant transactions.
    
    (See massage.ledgerize() for more info on the output of this method.)

    As a couresty, we WILL sort the transactions by date (as qb would...)
    """

    #basically, you can filter on any attribute massage.ledgerize() kicks out
    filterable_attributes = {
        "TxnDate":0, "qbbo_type":1, "entity_id":2, 
        "line_number":3, "document_type":4,
        "domain":5, "user_number":6,
        "CreateTime":7, "LastUpdatedTime":8, "SyncToken":9, "Adjustment":10,
        "account":11, "amount":13, "description":14, "name":15,
        "linked_transactions":16
    }

    line_i = filterable_attributes["line_number"]

    
    fa = copy.deepcopy(filter_attributes)

    for a in filter_attributes:
    
        if not a in filterable_attributes:
            raise Exception("QuickReport() doesn't know how to filter on"+
                            " %s. Please use one of:\n%s" % 
                            (a, filterable_attributes))
    
        #yes, we're being permissive
        if isinstance(filter_attributes[a],(int,float,long,str)):
            
            fa[a]=[filter_attributes[a]]

        elif isinstance(filter_attributes[a],(list,tuple)):
            
            fa[a]=filter_attributes[a]

        else:
            
            raise Exception("filter_attributes items must be lists," + \
                            "tuples, or stand-alone values")

    transactions = qbo_session.transactions()
    entity_list  = qbm.entity_list(transactions)
    ledger_lines_dict = {}

    for transaction in entity_list:

        qbbo, Id, _ = transaction

        this_transactions_lines = (qbo_session.ledgerize(transaction))

        for line in this_transactions_lines:

            k = qbbo+Id+str(line[line_i])

            ledger_lines_dict[k] = line


    #let's first sort by date...
    date_ordered_k_list = sorted(ledger_lines_dict.iterkeys(), key= \
                                 lambda k: ledger_lines_dict[k][0])

    filtered_lines = [qbo_session.ledgerize("_", headers=True)]
    
    for k in date_ordered_k_list:

        ledger_line = ledger_lines_dict[k]
        #print ledger_line

        #now let's apply the filter, white-list style

        for a in fa:

            white_list = fa[a]

            #sometimes a Line will just HAVE the attribute
            #e.g. a JournalEntry line will always have an account
            #othertimes, we'll have to look it up with a cross reference
            #e.g. an Invoice line will NOT have an account, it'll have
            #an item, so we need to look up the account in the item

            #so we're breaking that functionality out into it's own function

            i = filterable_attributes[a]

            if ledger_line[i] in white_list:

                filtered_lines.append(ledger_line)

    return filtered_lines

def pnl(qbo_session, start_date="first", end_date="last", period = "years"):

    raise NotImplementedError

def bs(qbo_session, first_date="first", last_date="last", period = "years"):

    raise NotImplementedError

def cf(qbo_session, start_date="first", end_date="last", period = "years"):

    raise NotImplementedError
