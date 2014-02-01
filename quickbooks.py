from rauth import OAuth1Session, OAuth1Service
import xml.etree.ElementTree as ET

import xmltodict

try:

    """
    This main module is for talking to the QBOv3 API. There are other
    supporting modules for doing stuff with the results or read and query
    operations and for getting stuff ready for update, delete,
    and create operations
    """

    import massage
    import reference
    import report

except:

    """
    There are convenience-function calls to these companion modules, all
    listed at the bottom here, and obvi those won't work alone, but
    the rest of this module should be standalone
    """

    pass

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

        if 'verbose' in args:
            self.verbose = True
        else:
            self.verbose = False

        self._BUSINESS_OBJECTS = ["Account","Attachable","Bill","BillPayment",
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

            # For some reason the totalCount isn't returned for some queries,
            # in that case, check the length, even though that actually requires
            # measuring
            try:
                result_count = int(r_dict['QueryResponse']['totalCount']) 
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

    def fetch_customer(self, pk):
        if pk:
            url = self.base_url_v3 + "/company/%s/customer/%s" % (self.company_id, pk)
            # url = self.base_url_v2 + "/resource/customer/v2/%s/%s" % ( self.company_id, pk)
            r_dict = self.keep_trying("GET", url, True, self.company_id)
            return r_dict['Customer']


    def fetch_customers(self, all=False, page_num=0, limit=10):
        if self.session != None:
            session = self.session
        else:
            session = self.create_session()
            self.session = session

        # Sometimes we use v2 of the API
        url = self.base_url_v2
        url += "/resource/customers/v2/%s" % (self.company_id)

        customers = []
        
        if all:
            counter = 1
            more = True

            while more:
                payload = {
                    "ResultsPerPage":30,
                    "PageNum":counter,
                    }

                trying = True

                # Because the QB API is so iffy, let's try until we get an non-error

                # Rewrite this to use same code as above.
                while trying:
                    r = session.request("POST", url, header_auth = True, data = payload, realm = self.company_id)
                    root = ET.fromstring(r.text)
                    if root[1].tag != "{http://www.intuit.com/sb/cdm/baseexceptionmodel/xsd}ErrorCode":
                        trying = False
                    else:
                        print "Failed"

                session.close()
                qb_name = "{http://www.intuit.com/sb/cdm/v2}"

                for child in root:
                    if child.tag == "{http://www.intuit.com/sb/cdm/qbo}Count":
                        
                        if int(child.text) < 30:
                            more = False
                            print "Found all customers"

                    if child.tag == "{http://www.intuit.com/sb/cdm/qbo}CdmCollections":
                        for customer in child:

                            customers += [xmltodict.parse(ET.tostring(customer))]
                                
                counter += 1

                # more = False

        else:

            payload = {
                "ResultsPerPage":str(limit),
                "PageNum":str(page_num),
                }

            r = session.request("POST", url, header_auth = True, data = payload, realm = self.company_id)

            root = ET.fromstring(r.text)

            #TODO: parse for all customers


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

    def query_objects(self, business_object, params={}, query_tail = ""):
        """
        Runs a query-type request against the QBOv3 API
        Gives you the option to create an AND-joined query by parameter
            or just pass in a whole query tail
        The parameter dicts should be keyed by parameter name and
            have twp-item tuples for values, which are operator and criterion
        """

        if business_object not in self._BUSINESS_OBJECTS:
            raise Exception("%s not in list of QBO Business Objects." %  \
                            business_object + " Please use one of the " + \
                            "following: %s" % self._BUSINESS_OBJECTS)

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

    def get_objects(self, qbbo, requery=False, params = {}, query_tail = ""):
        """
        Rather than have to look up the account that's associate with an
        invoice item, for example, which requires another query, it might
        be easier to just have a local dict for reference.

        The same is true with linked transactions, so transactions can
        also be cloned with this method
        """

        #we'll call the attributes by the Business Object's name + 's',
        #case-sensitive to what Intuit's documentation uses

        if qbbo not in self._BUSINESS_OBJECTS:
            raise Exception("%s is not a valid QBO Business Object." % qbbo) 

        attr_name = qbbo+"s"

        #if we've already populated this list, only redo if told to
        #because, say, we've created another Account or Item or something
        #during the session

        if not hasattr(self,attr_name) or requery:

            if self.verbose:
                print "Caching list of %ss." % qbbo

            object_list = self.query_objects(qbbo, params, query_tail)

            #let's dictionarize it (keyed by Id), though, for easy lookup later

            object_dict = {}

            for o in object_list:
                Id = o["Id"]

                object_dict[Id] = o

            setattr(self, attr_name, object_dict)
            
        return getattr(self,attr_name)

    def object_dicts(self, qbbo_list = [], requery=False,
                     params={}, query_tail=""):
        """
        returns a dict of lists of ALL the Business Objects of
        each of these types (filtering with params and query_tail)
        """

        object_dicts = {}       #{qbbo:[object_list]}

        for qbbo in qbbo_list:

            object_dicts[qbbo] = self.get_objects(qbbo,
                                                  requery,
                                                  params,
                                                  query_tail)

        return object_dicts

    def names(self, requery=False, params = {}, query_tail = ""):
        """
        get a dict of every Name List Business Object (of every type)

        results are subject to the filter if applicable

        returned dict has two dimensions:
        name = names[qbbo][Id]
        """
      

        name_list_objects = [
           "Account", "Class", "Customer", "Department", "Employee", "Item",
            "PaymentMethod", "TaxCode", "TaxRate", "Term", "Vendor"
        ]

        return self.object_dicts(name_list_objects, requery,
                                 params, query_tail)

    def transactions(self, requery=False, params = {}, query_tail = ""):
        """
        get a dict of every Transaction Business Object (of every type)

        results are subject to the filter if applicable

        returned dict has two dimensions:
        transaction = transactions[qbbo][Id]
        """
        transaction_objects = [
            "Bill", "BillPayment", "CreditMemo", "Estimate", "Invoice",
            "JournalEntry", "Payment", "Purchase", "PurchaseOrder", 
            "SalesReceipt", "TimeActivity", "VendorCredit"
        ]

        return self.object_dicts(transaction_objects, requery,
                                        params, query_tail)

    # -------------------------------------------------------------
    #below are the convenience-function calls that have dependencies
    # -------------------------------------------------------------

    def quick_report(self, filter_attributes = {}):
        """see report.quick_report.__doc__"""

        return report.quick_report(self, filter_attributes)

    def ledgerize(self, transaction, headers=False):
        """see ledgerize.__doc__ in the massage module"""
        
        return massage.ledgerize(transaction, self, headers)
                    
    def listize(self,name, headers=False):
        """see name_list.__doc__ in the massage module"""
        
        raise NotImplementedError

        return massage.listize(name_list_item, self, headers)

    def entity_list(self,raw_entities_dict):
        """see entity_list.__doc__ in the massage module"""

        return massage.entity_list(raw_entities_dict)

    def get_entity(self, qbbo, entity_id):
        """
        Note that this queries all objects of this type (for later convenience)!
        
        Creates (or refers to an attribute that's) a dictionary
         of all entities (names and transactions) keyed by
         Id (because every object has a unique one).
        
        Returns a tuple in the form (qbbo_type, raw_object_dict)
        """
        if not hasattr(self, qbbo+"s"):

            self.get_objects(qbbo)

        return getattr(self,qbbo+"s")[entity_id]

    def get_ap_account(self,name=False):
        """
        In QBO, you can only use one A/P account with "Bills" (though you can
        pro'ly use others with JEs and other entries if you want to.
        
        This figures out which A/P account that is (by ID)
        """
        if not hasattr(self,"ap_account_id"):
            
            Bills        = self.get_objects("Bill")

            first_bill   = Bills[Bills.keys()[0]]

            self.ap_account_id = first_bill["APAccountRef"]["value"]
            self.ap_account_name   = first_bill["APAccountRef"]["name"]

        if name:
            return self.ap_account_name
        else:
            return self.ap_account_id

    def get_ar_account(self,name=False):
        """
        Haven't found anything that actually shows the AR account in QBO...
        """
        return "Accounts Receivable"
