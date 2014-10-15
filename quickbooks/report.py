"""
This module is for API consumer-side reporting on QBOv3-querried transactions.
 In addition to mimmicking such features as "QuickReport," "General Ledger,"
 "Profit & Loss," et al, it provides some helpful functions, such as finding
 the starting and ending balance of a particular account as of a particular
 date and, of course, finding the total activity between two dates.
"""

import copy
import calendar
from dateutil.rrule import *
from dateutil.parser import *
from datetime import *
"""
get the right version of dateutil here:
http://labix.org/python-dateutil#head-2f49784d6b27bae60cde1cff6a535663cf87497b
"""

import reference as qbrefs
import massage   as qbm

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

    filtered_lines = [qbo_session.ledgerize("_", headers=True)]

    for ledger_line in qbo_session.ledger_lines():

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

def chart_of_accounts(qbo_session, attrs = "strict"):
    """
    Make a tabular data sctructure representing all of a company's 
    accounts.
    """

    #query all the accounts
    accounts = qbo_session.get_objects("Account")

    #by strict, I mean the order the docs say to use when udpating:
    #https://developer.intuit.com/docs/0025_quickbooksapi/
    #0050_data_services/030_entity_services_reference/account

    if attrs == "strict":
        attrs = [
            "Id", "SyncToken", "MetaData", "Name", "SubAccount",
            "ParentRef", "Description", "FullyQualifiedName", "Active",
            "Classification", "AccountType", "AccountSubType", "AcctNum",
            "OpeningBalance", "OpeningBalanceDate", "CurrentBalance",
            "CurentBalanceWithSubAccounts", "CurrencyRef"
        ]

    else:
        #TODO: validate the attrs against the 'strict' list above
        pass

    #As a first cut, we'll sort them by AccountType in trial balance order

    tb_type_order = [
        "Bank", "Accounts Receivable", "Other Current Asset",
        "Fixed Asset", "Other Asset",
        "Accounts Payable", "Credit Card",
        "Other Current Liability", "Other Liability",
        "Equity",
        "Income", "Other Income",
        "Expense", "Other Expense", "Cost of Goods Sold"
    ]

    accounts_by_type = {} #{Accounts_Payable:[row_list]

    for a_id in accounts:
        a = accounts[a_id]
        at = a["AccountType"]
        if at not in tb_type_order:
            raise Exception("Unexpected AccountType: %s" % at)

        if at not in accounts_by_type:
            accounts_by_type[at]=[]

        this_row = []
        for field in attrs:
            if field not in a:
                this_row.append("")
            else:
                value = a[field]
                if isinstance(value,(list,tuple,dict)):
                    this_row.append("<complex>")
                else:
                    this_row.append(a[field])

        accounts_by_type[at].append(this_row)

    rows = [attrs]                     #headers are the first row
    for at in tb_type_order:
        if at in accounts_by_type:
            for row in accounts_by_type[at]:
                rows.append(row)

    return rows

def name_list(qbo_session):
    """
    Generate a tabular list of all Vendors, Customers, and Employees that can be
     referenced by other transactions (when uploading a JE, e.g.).
    """

    return qbo_session.name_list()
    

def pnl(qbo_session, period = "YEARLY", start_date="first", end_date="last",
        **kwargs):
    """
    start_date and end_dates should be datetime objects if they're to be used

    kwargs are for filtering the QUERY, not the report here (and other
    functionality too...see below)
    """

    pnl_account_types = [
        
        "Income", "Other Income",
        "Expense", "Other Expense", "Cost of Goods Sold"
        
    ]

    

    # go through the accounts, collecting a list of those that are 
    # pnl accounts

    relevant_accounts = []

    coa = qbo_session.chart_of_accounts()

    AccountType_i = coa[0].index("AccountType")
    fqa_i = coa[0].index("FullyQualifiedName")

    for a in coa:

        AccountType = a[AccountType_i]

        if AccountType in pnl_account_types:

            relevant_accounts.append(a[fqa_i])
   
    # now collect the ledger_lines that are even relevant to the time
    # period and pnl accounts (and we'll handle presentation last)

    relevant_activity = {} #{account:[relevant lines]}

    all_ledger_lines  = qbo_session.ledger_lines(None, None, None, True,
                                                 **kwargs)

    headers = all_ledger_lines[0]

    account_i = headers.index("account")  
    amount_i  = headers.index("amount")
    date_i    = headers.index("TxnDate")
    
    earliest_date = datetime(2100,1,1)
    latest_date   = datetime(1900,1,1)

    for line in all_ledger_lines[1:]:

        account = line[account_i]
        line_date    = line[date_i]

        #first apply the date filter!
        if not start_date == "first" and line_date < start_date:
            continue
            
        if not end_date == "last" and line_date > end_date:
            continue
        
        #if it's made the cut, we can update the report date bounds
        earliest_date = min(line_date,earliest_date)
        latest_date   = max(line_date,latest_date)

        #then apply the account filter!

        if not account in relevant_activity:
            #then let's confirm that its account type is a pnl one
            
            if not account in relevant_accounts:
                
                continue

            else:
                relevant_activity[account] = []

        relevant_activity[account].append(line)

    #now let's do presentation
    #TODO -- incorporate pandas tables...do only minimal work on it until then

    pnl_lines = []

    if period == "YEARLY":

        report_start_date = datetime(earliest_date.year,1,1)
        report_end_date   = datetime(latest_date.year,12,31)

        period_start_dates = list(rrule(YEARLY, bymonth=1, bymonthday=1,
                                        dtstart=report_start_date,
                                        until=report_end_date))

        period_end_dates   = list(rrule(YEARLY, bymonth=12, bymonthday=-1,
                                        dtstart=report_start_date,
                                        until=report_end_date))

    elif period == "MONTHLY":

        report_start_date = datetime(earliest_date.year,
                                     earliest_date.month,
                                     1)
        report_end_date   = datetime(latest_date.year,
                                     latest_date.month,
                                     calendar.monthrange(latest_date.year,
                                                         latest_date.month)[1])

        period_start_dates = list(rrule(MONTHLY, bymonthday=1,
                                        dtstart=report_start_date,
                                        until=report_end_date))

        period_end_dates   = list(rrule(YEARLY, bymonthday=-1,
                                        dtstart=report_start_date,
                                        until=report_end_date))       

    header_1 = ["", "Period Start -->"]      + period_start_dates
    header_2 = ["Account", "Period End -->"] + period_end_dates

    pnl_lines.append(header_1)
    pnl_lines.append(header_2)

    """Clearly, there's a way to do this with only one pass of the data...
    let's get that right in the first re-write...probably with pandas"""

    #now let's fill up the pnl_lines with what we know to be the relevant data
    #for now, we'll rely on the knowledge that the data is coming to us in
    #date order, but that should be fixed too...

    for account in relevant_activity:

        account_row = [account, ""]    #one value per period 

        current_period_index = 0    #primitive counter, yes!
        this_period_total    = 0    #this will be this period's total

        for line in relevant_activity[account]:
            
            line_amount      = line[amount_i]
            line_date        = line[date_i] 

            if line_date > period_end_dates[current_period_index]:

                account_row.append(this_period_total)
                this_period_total     = line_amount
                current_period_index +=1

            else:
                
                this_period_total     = round(this_period_total +
                                              line_amount, 2)

        """super sloppy..."""
        account_row.append(this_period_total)   #for the last period
        current_period_index +=1

        while current_period_index < len(period_end_dates):
            account_row.append(0)
            current_period_index +=1

        pnl_lines.append(account_row)

    return pnl_lines

def bs(qbo_session, first_date="first", last_date="last", period = "years"):

    bs_account_types = [
        
        "Bank", "Accounts Receivable", "Other Current Asset", "Fixed Asset",
        "Other Asset"
        "Accounts Payable", "Credit Card", "Other Current Liability",
        "Other Liability",
        "Equity"

    ]

    raise NotImplementedError

def cf(qbo_session, start_date="first", end_date="last", period = "years"):

    raise NotImplementedError
