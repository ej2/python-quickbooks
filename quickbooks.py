from rauth import OAuth1Session, OAuth1Service
import xml.etree.ElementTree as ET

import xmltodict

class QuickBooks():
    """A wrapper class around Python's Rauth module for Quickbooks the API"""

    access_token = ''
    access_token_secret = ''
    consumer_key = ''
    consumer_secret = ''
    company_id = 0
    callback_url = ''
    session = None

    base_url_v3 =  "https://quickbooks.api.intuit.com/v3"
    base_url_v2 = "https://qbo.intuit.com/qbo1"

    request_token_url = "https://oauth.intuit.com/oauth/v1/get_request_token"
    access_token_url = "https://oauth.intuit.com/oauth/v1/get_access_token"

    authorize_url = "https://appcenter.intuit.com/Connect/Begin"

    # Things needed for authentication
    qbService = None

    request_token = ''
    request_token_secret = ''

    def __init__(self, **args):

        if 'cred_path' in args:
            self.read_creds_from_file(args['cred_path'])

        if 'consumer_key' in args:
            self.consumer_key = args['consumer_key']

        if 'consumer_secret' in args:
            self.consumer_secret = args['consumer_secret']
                                   
        if 'access_token' in args:
            self.access_token = args['access_token']

        if 'access_token_secret' in args:
            self.access_token_secret = args['access_token_secret']

        if 'company_id' in args:
            self.company_id = args['company_id']
        
        if 'callback_url' in args:
            self.callback_url = args['callback_url']

        self.BUSINESS_OBJECTS = ["Account","Attachable","Bill","BillPayment",
                                "Class","CompanyInfo","CreditMemo","Customer",
                                "Department","Employee","Estimate","Invoice",
                                "Item","JournalEntry","Payment","PaymentMethod",
                                "Preferences","Purchase","PurchaseOrder",
                                "SalesReceipt","TaxCode","TaxRate","Term",
                                "TimeActivity","Vendor","VendorCredit"]


    def get_authorize_url(self):
        """Returns the Authorize URL as returned by QB, 
        and specified by OAuth 1.0a.
        :return URI:
        """
        self.qbService = OAuth1Service(
                name = None,
                consumer_key = self.consumer_key,
                consumer_secret = self.consumer_secret,
                request_token_url = self.request_token_url,
                access_token_url = self.access_token_url,
                authorize_url = self.authorize_url,
                base_url = None
            )
        self.request_token, self.request_token_secret = self.qbService.get_request_token(
                params={'oauth_callback':self.callback_url}
            )

        return self.qbService.get_authorize_url(self.request_token)

    def get_access_tokens(self, oauth_verifier):
        """Wrapper around get_auth_session, returns session, and sets 
        access_token and access_token_secret on the QB Object.
        :param oauth_verifier: the oauth_verifier as specified by OAuth 1.0a
        """
        session = self.qbService.get_auth_session(
                self.request_token, 
                self.request_token_secret,
                data={'oauth_verifier': oauth_verifier})

        self.access_token = session.access_token
        self.access_token_secret = session.access_token_secret

        return session

    def create_session(self):
        if self.consumer_secret and self.consumer_key and self.access_token_secret and self.access_token:
            session = OAuth1Session(self.consumer_key,
                self.consumer_secret,
                self.access_token,
                self.access_token_secret,
                )
            self.session = session
        else:
            raise Exception("Need four creds for Quickbooks.create_session.")
        return self.session

    def query_fetch_more(self, r_type, header_auth, realm, qb_object, original_payload =''):
        """ Wrapper script around keep_trying to fetch more results if 
        there are more. """
        
        # 500 is the maximum number of results returned by QB

        max_results = 500
        start_position = 0
        more = True
        data_set = []
        url = self.base_url_v3 + "/company/%s/query" % self.company_id

        # Edit the payload to return more results.
        
        payload = original_payload + " MAXRESULTS " + str(max_results)
        
        while more:
            
            r_dict = self.keep_trying(r_type, url, True, self.company_id, payload)

            try:
                access = r_dict['QueryResponse'][qb_object]
            except:
                if 'QueryResponse' in r_dict and r_dict['QueryResponse'] == {}:
                    #print "Query OK, no results: %s" % r_dict['QueryResponse']
                    return []
                else:
                    print "FAILED", r_dict
                    r_dict = self.keep_trying(r_type,
                                              url,
                                              True,
                                              self.company_id,
                                              payload)

            # Check the returned maxResults to see how many results are
            # in the query. 
            try:
                result_count = int(r_dict['QueryResponse']['maxResults']) 
                if result_count < max_results:
                    more = False
            except KeyError:
                try:
                    result_count = len(r_dict['QueryResponse'][qb_object]) 
                    if result_count < max_results:
                        more = False
                except KeyError:
                    print "\n\n ERROR", r_dict
                    pass

            # Just some math to prepare for the next iteration
            if start_position == 0:
                start_position = 1

            start_position = start_position + max_results
            payload = "%s STARTPOSITION %s MAXRESULTS %s" % (original_payload, 
                    start_position, max_results)


            data_set += r_dict['QueryResponse'][qb_object]

        #print "Records Found: %d." % len(data_set)
        return data_set

    def keep_trying(self, r_type, url, header_auth, realm, payload=''):
        """ Wrapper script to session.request() to continue trying at the QB
        API until it returns something good, because the QB API is 
        inconsistent """
        if self.session != None:
            session = self.session
        else:
            session = self.create_session()
            self.session = session

        trying = True
        tries = 0
        while trying:
            tries += 1
            if "v2" in url:
                r = session.request(r_type, url, header_auth, realm, data=payload)
                
                r_dict = xmltodict.parse(r.text)
                
                if "FaultInfo" not in r_dict or tries > 4:
                    trying = False
            else:
                headers = {
                        'Content-Type': 'application/text',
                        'Accept': 'application/json'
                    }

                #print r_type,url,header_auth,realm,headers,payload
                #quit()
                r = session.request(r_type, url, header_auth, realm, headers = headers, data = payload)
                
                r_dict = r.json()

                if "Fault" not in r_dict or tries > 4:
                    trying = False
                elif "Fault" in r_dict and r_dict["Fault"]["type"]==\
                     "AUTHENTICATION":
                    #Initially I thought to quit here, but actually
                    #it appears that there are 'false' authentication
                    #errors all the time and you just have to keep trying...
                    trying = True

        return r_dict

    def query_object(self,business_object,params={}, query_tail = ""):
        """
        Runs a query-type request against the QBOv3 API
        Gives you the option to create an AND-joined query by parameter
            or just pass in a whole query tail
        The parameter dicts should be keyed by parameter name and
            have two-item tuples for values, which are operator and criterion
        """

        if business_object not in self.BUSINESS_OBJECTS:
            raise Exception("%s not in list of QBO Business Objects." %  \
                            business_object + " Please use one of the " + \
                            "following: %s" % self.BUSINESS_OBJECTS)

        #eventually, we should be able to select more than just *,
        #but chances are any further filtering is easier done with Python
        #than in the query...

        query_string="SELECT * FROM %s" % business_object
        
        if query_tail == "" and not params == {}:

            #It's not entirely obvious what are valid properties for
            #filtering, so we'll collect the working ones here and
            #validate the properties before sending it
            #datatypes are defined here:
            #https://developer.intuit.com/docs/0025_quickbooksapi/
            #    0050_data_services/020_key_concepts/0700_other_topics

            props = {
                "TxnDate":"Date",
                "MetaData.CreateTime":"DateTime",      #takes a Date though
                "MetaData.LastUpdatedTime":"DateTime"  #ditto
            }

            p = params.keys()
            
            #only validating the property name for now, not the DataType
            if p[0] not in props:
                raise Exception("Unfamiliar property: %s" % p[0])

            query_string+=" WHERE %s %s %s" % (p[0],
                                               params[p[0]][0],
                                               params[p[0]][1])

            if len(p)>1:
                for i in range(1,len(p)+1):
                    if p[i] not in props:
                        raise Exception("Unfamiliar property: %s" % p[i])
                    
                    query_string+=" AND %s %s %s" % (p[i],
                                                     params[p[i]][0],
                                                     params[p[i]][1])

        elif not query_tail == "":
            if not query_tail[0]==" ":
                query_tail = " "+query_tail
            query_string+=query_tail

        #CAN ONE SESSION USE MULTIPLE COMPANIES?
        #IF NOT, REMOVE THE COMPANY OPTIONALITY
        url = self.base_url_v3 + "/company/%s/query" % self.company_id

        results = self.query_fetch_more(r_type="POST",
                                        header_auth=True,
                                        realm=self.company_id,
                                        qb_object=business_object,
                                        original_payload=query_string)

        return results

    def fetch_customer(self, pk):
        if pk:
            url = self.base_url_v3 + "/company/%s/customer/%s" % (self.company_id, pk)
            # url = self.base_url_v2 + "/resource/customer/v2/%s/%s" % ( self.company_id, pk)
            r_dict = self.keep_trying("GET", url, True, self.company_id)
            return r_dict['Customer']


    def fetch_customers(self, all=False, page_num=0, limit=10):
        """ Use self.query_object to access all the customers 
        TODO: add query for 'all'
        """
        #query all the customers
        customers = self.query_object("Customer")

        return customers

    def fetch_sales_term(self, pk):
        if pk:
            url = self.base_url_v2 + "/resource/sales-term/v2/%s/%s" % ( self.company_id, pk)
            r_dict = self.keep_trying("GET", url, True, self.company_id)
            return r_dict


    def fetch_invoices(self, **args):
        qb_object = "Invoice"
        payload = "SELECT * FROM %s" % (qb_object)
        if "query" in args:
            if "customer" in args['query']:
                payload = ("SELECT * FROM %s WHERE "
                    "CustomerRef = '%s'") % (
                        qb_object, args['query']['customer']
                        )

        r_dict = self.query_fetch_more("POST", True, 
                self.company_id, qb_object, payload)

        return r_dict
        

    def fetch_purchases(self, **args):
        # if "query" in args:
            qb_object = "Purchase"
            payload = ""
            if "query" in args and "customer" in args['query']:

                # if there is a customer, let's get the create date 
                # for that customer in QB, all relevant purchases will be
                # after that date, this way we need less from QB

                customer = self.fetch_customer(args['query']['customer'])

                # payload = "SELECT * FROM %s" % (qb_object)
                payload = "SELECT * FROM %s WHERE MetaData.CreateTime > '%s'"% (
                        qb_object, 
                        customer['MetaData']['CreateTime']
                        )

            else:
                payload = "SELECT * FROM %s" % (qb_object)

            unfiltered_purchases = self.query_fetch_more("POST", True, 
                self.company_id, qb_object, payload)

            filtered_purchases = []

            if "query" in args and "customer" in args['query']:
                for entry in unfiltered_purchases:

                    if (
                        'Line' in entry
                        ):
                        for line in entry['Line']:
                            if (
                                'AccountBasedExpenseLineDetail' in line and 
                                'CustomerRef' in line['AccountBasedExpenseLineDetail'] and
                                line['AccountBasedExpenseLineDetail']['CustomerRef']['value'] == args['query']['customer']
                                ):
                                
                                filtered_purchases += [entry]

                        
                return filtered_purchases
            else:
                return unfiltered_purchases

    def fetch_journal_entries(self, **args):
        """ Because of the beautiful way that journal entries are organized
        with QB, you're still going to have to filter these results for the
        actual entity you're interested in.

        :param query: a dictionary that includes 'customer', and the QB id of the
            customer
        """

        payload = {}
        more = True
        
        journal_entries = []
        max_results = 500
        start_position = 0

        if "query" in args and "project" in args['query']:
            original_payload = "SELECT * FROM JournalEntry"

        elif "query" in args and "raw" in args['query']:
            original_payload = args['query']['raw']

        else:
            original_payload = "SELECT * FROM JournalEntry"

        payload = original_payload + " MAXRESULTS " + str(max_results)

        while more:

            url = self.base_url_v3 + "/company/%s/query" % (self.company_id)

            r_dict = self.keep_trying("POST", url, True, self.company_id, payload)
            
            if int(r_dict['QueryResponse']['totalCount']) < max_results:
                more = False
            if start_position == 0:
                start_position = 1
            start_position = start_position + max_results
            payload = "%s STARTPOSITION %s MAXRESULTS %s" % (original_payload, start_position, max_results)
            journal_entry_set = r_dict['QueryResponse']['JournalEntry']
            
            # This has to happen because the QBO API doesn't support 
            # filtering along customers apparently.
            if "query" in args and "class" in args['query']:
                for entry in journal_entry_set:
                    for line in entry['Line']:
                        if 'JournalEntryLineDetail' in line:
                            if 'ClassRef' in line['JournalEntryLineDetail']:
                                if args['query']['class'] in line['JournalEntryLineDetail']['ClassRef']['name']:
                                    journal_entries += [entry]
                                    break
            else:
                journal_entries = journal_entry_set

        return journal_entries


    def fetch_bills(self, **args):
        """Fetch the bills relevant to this project."""
        # if "query" in args:
        payload = {}
        more = True
        counter = 1
        bills = []
        max_results = 500
        start_position = 0
        if "query" in args and "customer" in args['query']:
            original_payload = "SELECT * FROM Bill"
        elif "query" in args and "raw" in args['query']:
            original_payload = args['query']['raw']
        else:
            original_payload = "SELECT * FROM Bill"

        payload = original_payload + " MAXRESULTS " + str(max_results)

        while more:

            url = self.base_url_v3 + "/company/%s/query" % (self.company_id)
            
            r_dict = self.keep_trying("POST", url, True, self.company_id, payload)
            counter = counter + 1
            if int(r_dict['QueryResponse']['maxResults']) < max_results:
                more = False

            #take into account the initial start position
            if start_position == 0:
                start_position = 1
            start_position = start_position + max_results

            # set new payload
            payload = "%s STARTPOSITION %s MAXRESULTS %s" % (
                original_payload, 
                start_position, 
                max_results)
            bill = r_dict['QueryResponse']['Bill']

            # This has to happen because the QBO API doesn't support 
            # filtering along customers apparently.
            if "query" in args and "class" in args['query']:

                for entry in bill:

                    for line in entry['Line']:

                        if 'AccountBasedExpenseLineDetail' in line:
                            line_detail = line['AccountBasedExpenseLineDetail']

                            if 'ClassRef' in line_detail:
                                name = line_detail['ClassRef']['name']

                                if args['query']['class'] in name:
                                    bills += [entry]
                                    break
            else:
                bills += bill
        # print bills
        return bills

    def chart_of_accounts(self, attrs = "strict"):
        """make a tabular data sctructure representing all of a company's 
        accounts."""
        
        #query all the accounts
        accounts = self.query_object("Account")

        #by strict, I mean the order the docs say to use when udpating:
        #https://developer.intuit.com/docs/0025_quickbooksapi/0050_data_services/030_entity_services_reference/account

        if attrs == "strict":
            attrs = [
                "Id", "SyncToken", "MetaData", "Name", "SubAccount",
                "ParentRef", "Description", "FullyQualifiedName", "Active",
                "Classification", "AccountType", "AccountSubType", "AcctNum",
                "OpeningBalance", "OpeningBalanceDate", "CurrentBalance",
                "CurentBalanceWithSubAccounts", "CurrencyRef"
            ]
            
        #As a first cut, we'll sort them by AccountType in trial balance order
        
        tb_type_order = [
            "Bank", "Accounts Receivable", "Other Current Asset",
            "Fixed Asset", "Other Asset",
            "Accounts Payable", "Credit Card", "Long Term Liability",
            "Other Current Liability",
            "Equity",
            "Income", "Other Income",
            "Cost of Goods Sold", "Expense", "Other Expense"
        ]
        
        accounts_by_type = {} #{Accounts_Payable:[row_list]
        
        for a in accounts:
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

    def quick_report(self, params={}, query_tail=""):
        """
        Simulates a 'Quick Report' in QB by pulling down all transactions
        that touch the account we're passed.
        
        Allows (or should eventually allow) date, class, and other filters.
        """
        

        transaction_objects = [
            "Bill", "BillPayment", "CreditMemo", "Estimate", "Invoice",
            "JournalEntry", "Payment", "Purchase", "PurchaseOrder", 
            "SalesReceipt", "TimeActivity", "VendorCredit"
        ]

        transactions = {}   #{qbbo:[trnslist]}

        #transaction_objects = ["JournalEntry"]  #shortlist for debugging stuff

        for qbbo in transaction_objects:
            print "Querying %ss" % qbbo
            results = self.query_object(qbbo,params,query_tail)
            if results == []:
                #no txns of this type in the result set...
                continue
            else:
                transactions[qbbo]=results

        return transactions

    def ledgerize(self,transaction,qbbo=None):
        """
        Takes a transaction Business Object (BillPayment, Purchase,
        whatever), and returns a tabular data structure that identifies the
        transaction, much like a set of general ledger lines

        Where capital letters are used in variable names, it's generally
        to indicate that it's the case-faithful QuickBooks business object
        property name...sorry I'm breaking the naming conventions, but
        I think it's worth it to avoid confusion here
        """

        #first let's set the common properties (required then optional)

        document_number          = transaction["Id"]
        TxnDate                  = transaction["TxnDate"]
        CreateTime               = transaction["MetaData"]["CreateTime"] 
        LastUpdatedTime          = transaction["MetaData"]["LastUpdatedTime"] 
        SyncToken                = transaction["SyncToken"]
        domain                   = transaction["domain"]
        #add department!
        
        if "PrivateNote" in transaction:
            head_description     = transaction["PrivateNote"]
        else:
            head_description      = ""

        if "DocNumber" in transaction:
            reference            = transaction["DocNumber"]
        else:
            reference            = ""

        if "LinkedTxn" in transaction:

            linked_transactions  = []

            for lt in transaction["LinkedTxn"]:
                lt_doc           = lt["TxnType"]
                lt_num           = lt["TxnId"]
                linked_transactions.append(lt_doc+"/"+lt_num)

            linked_transactions  = "; ".join(linked_transactions)

        else:
            linked_transactions  = ""

        if "TotalAmt" in transaction:
            TotalAmt             = transaction["TotalAmt"]
        #else, it's a JournalEntry and has no TotalAmt...

        #now let's deal with properties unique to certain objects

        if qbbo == "Bill":

            document_type = "Bill"
            #head_account  = transaction["APAccountRef"]["name"]
            """
            really, it maybe be possible to rename and/or have more than
            one AP account, but because BillPayment objects don't show
            account information at the split level, it's probably a look-up
            operation (to the linked transaction) to figure it out.
            Hence, we're going the easy route and assuming the thing is just
            called "Accounts Payable."
            """
            head_account     = "Accounts Payable"
            name             = transaction["VendorRef"]["name"]
            polarity         = "Credit"

        elif qbbo == "BillPayment":

            document_type    = transaction["PayType"]

            #Some "BillPayments" just represent "applying a payment,"
            #where a check or other item is matched to an oustanding
            #bill. In this case, whatever entry is so matched ALREADY
            #must have debited accounts payable, so we're going to just
            #keep this entry for the transaction linkages (important!)
            #We'll be debiting AND crediting A/P in the same entry...

            if "BankAccountRef" not in transaction["CheckPayment"]:
                head_account = "Accounts Payable"
            else:
                head_account = transaction["CheckPayment"]\
                                   ["BankAccountRef"]["name"]

            name             = transaction["VendorRef"]["name"]
            polarity         = "Credit"

        elif qbbo == "Invoice":

            document_type    = "Invoice"
            #account isn't explicitly stated, so...
            head_account     = "Accounts Receivable"
            name             = transaction["CustomerRef"]["name"]
            polarity         = "Debit"    

        elif qbbo == "JournalEntry":

            document_type    = "JournalEntry"

        elif qbbo == "Purchase":
            
            document_type    = transaction["PaymentType"]
            head_account     = transaction["AccountRef"]["name"]

            #CC charges, e.g., don't have to have a name...

            if "EntityRef" not in transaction:
                name         = ""
            else:
                name         = transaction["EntityRef"]["name"]

            polarity         = "Credit"
            
        else:
                
            raise NotImplementedError("Implement QuickBooks.ledgerize()"+\
                                      " for %s objects!" % qbbo)
            

        ledger_lines = []

        #add headers:
        ledger_lines.append([              
            "TxnDate", "document_type", "document_number", "line_number", 
            "domain", "reference",
            "CreateTime", "LastUpdatedTime", "SyncToken",
            "head_account", "amount", "head_description", "name",
            "linked_transactions"
        ])

        #JournalEntries, uniquely, have no 'header', so their first line
        #(which QB labels with Id=0) is the the first 'Line'
        #for all other object types though:
        
        if not qbbo in "JournalEntry":

            #QB shows all amounts as positive (like many GL systems)
            #For simplicity, it's sometimes easier to have credits simply
            #appear as negative numbers, so we're flipping the sign of the
            #amounts as necessary....        

            if polarity == "Credit":
                amount = -TotalAmt
            else:
                amount = TotalAmt

            ledger_lines.append([
                TxnDate, document_type, document_number, 0,  #zero-indexed!
                domain, reference,
                CreateTime, LastUpdatedTime, SyncToken,
                head_account, amount, head_description, name,
                linked_transactions
            ])
        
        #because one (or maybe a few) object types don't include line Ids,
        #we have to count them
        
        this_line_number = 0

        for split_line in transaction["Line"]:

            this_line_number+=1

            #first the common properties, again
            Amount                   = split_line['Amount']
            
            if "Id" in split_line:
                line_number          = split_line["Id"]
            else:
                line_number          = this_line_number
                
            if "Description" not in split_line:
                Description      = ""
            else:
                Description      = split_line["Description"]

            if "LinkedTxn" in split_line:
                linked_transactions = []
            
                for lt in split_line["LinkedTxn"]:
                    lt_doc           = lt["TxnType"]
                    lt_num           = lt["TxnId"]
                    linked_transactions.append(lt_doc+"/"+lt_num)

                linked_transactions  = "; ".join(linked_transactions)

            else:
                linked_transactions  = ""

            #add class!

            #now on to object-specific properties
    
            if qbbo == "Bill":

                account  = split_line["AccountBasedExpenseLineDetail"]\
                          ["AccountRef"]["name"]
                polarity             = "Debit"

            elif qbbo == "BillPayment":

                #AP, per above, is kind of a special case
                account              = "Accounts Payable"
                polarity             = "Debit"
                
            elif qbbo == "Invoice":
                
                #we only want SalesItemLineDetail split_lines
                if not split_line["DetailType"] == "SalesItemLineDetail":
                    continue

                item                 = split_line["SalesItemLineDetail"]\
                                       ["ItemRef"]["name"]
                #this lookup functionality needs to query / read an "Item"
                account              = "Look account for Item %s!" % item
                polarity             = "Credit"
                
            elif qbbo == "JournalEntry":
                
                je_deets             = split_line["JournalEntryLineDetail"]

                account              = je_deets["AccountRef"]["name"]
                if "Entity" in je_deets:
                    name             = je_deets["Entity"]["EntityRef"]["name"]
                else:
                    name             = ""

                polarity             = je_deets["PostingType"]

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
                TxnDate, document_type, document_number, line_number,
                domain, reference,
                CreateTime, LastUpdatedTime, SyncToken,
                account, amount, Description, name,
                linked_transactions
            ])
                                
        return ledger_lines
        
                    
