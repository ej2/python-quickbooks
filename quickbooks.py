'''Main class'''
import xml.etree.ElementTree as ET

import json

try:
    from rauth import OAuth1Session, OAuth1Service
except:
    print("Please import Rauth:\n\n")
    print("http://rauth.readthedocs.org/en/latest/\n")

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

except ImportError:

    print("You won't be able to run some of the additional methods")

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

        self._BUSINESS_OBJECTS = [

            "Account","Attachable","Bill","BillPayment",
            "Class","CompanyInfo","CreditMemo","Customer",
            "Department","Employee","Estimate","Invoice",
            "Item","JournalEntry","Payment","PaymentMethod",
            "Preferences","Purchase","PurchaseOrder",
            "SalesReceipt","TaxCode","TaxRate","Term",
            "TimeActivity","Vendor","VendorCredit"

        ]


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
        if (self.consumer_secret and 
            self.consumer_key and 
            self.access_token_secret and 
            self.access_token):
            session = OAuth1Session(self.consumer_key,
                self.consumer_secret,
                self.access_token,
                self.access_token_secret,
                )
            self.session = session
        else:
            raise Exception("Need four creds for Quickbooks.create_session.")
        return self.session

    def query_fetch_more(self, r_type, header_auth, realm, qb_object, 
        original_payload =''):
        """ Wrapper script around keep_trying to fetch more results if 
        there are more. """

        # 500 is the maximum number of results returned by QB

        max_results = 500
        start_position = 0
        more = True
        data_set = []
        url = self.base_url_v3 + "/company/{}/query".format(self.company_id)

        # Edit the payload to return more results.
        
        payload = original_payload + " MAXRESULTS " + str(max_results)
        
        while more:
            
            r_dict = self.hammer_it(r_type,
                                    url, 
                                    payload, 
                                    "text"
                                    )

            try:
                access = r_dict['QueryResponse'][qb_object]
            except:
                if 'QueryResponse' in r_dict and r_dict['QueryResponse'] == {}:
                    #print "Query OK, no results: %s" % r_dict['QueryResponse']
                    return []
                else:
                    print("FAILED", r_dict)
                    r_dict = self.hammer_it(r_type,
                                              url,
                                              payload,
                                              "text"
                                              )

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
                    print("\n\n ERROR", r_dict)
                    pass

            # Just some math to prepare for the next iteration
            if start_position == 0:
                start_position = 1

            start_position = start_position + max_results
            payload = "{0} STARTPOSITION {1} MAXRESULTS {2}".format(original_payload, 
                    start_position, max_results)


            data_set += r_dict['QueryResponse'][qb_object]

        #print "Records Found: %d." % len(data_set)
        return data_set

    def create_object(self, qbbo, request_body, content_type = "json"):
        """
        One of the four glorious CRUD functions.
        Getting this right means using the correct object template and
        and formulating a valid request_body. This doesn't help with that.
        It just submits the request and adds the newly-created object to the
        session's brain.
        """
    
        if qbbo not in self._BUSINESS_OBJECTS:
            raise Exception("{} is not a valid QBO Business Object." % qbbo,
                            " (Note that this validation is case sensitive.)")

        url = "https://qb.sbfinance.intuit.com/v3/company/{0}/{1}".format(
              self.company_id, qbbo.lower())

        if self.verbose:

            print("About to create a %s object with this request_body:".format(\
                qbbo))
            print(request_body)

        new_object = self.hammer_it("POST", url, request_body, content_type)\
                     [qbbo]

        new_Id     = new_object["Id"]

        attr_name = qbbo+"s"

        if not hasattr(self,attr_name):

            if self.verbose:
                print("Creating a %ss attribute for this\
                    session.".format(qbbo))

            setattr(self, attr_name, {new_Id:new_object})

        else:

            if self.verbose:
                print("Adding this new %s to the existing set of them.".format(
                    qbbo))
                print(json.dumps(new_object, indent=4))

            getattr(self, attr_name)[new_Id] = new_object

        return new_object

    def read_object(self, qbbo, object_id):
        """Makes things easier for an update because you just do a read,
        tweak the things you want to change, and send that as the update
        request body (instead of having to create one from scratch)."""

        pass

    def update_object(self, qbbo, object_id, request_body,
                      content_type = "json"):
        """Generally before calling this, you want to call the read_object
        command on what you want to update. The alternative is forming a valid
        update request_body from scratch, which doesn't look like fun to me."""

        pass

    def delete_object(self, qbbo, request_body, content_type = "json"):
        """Don't need to give it an Id, just the whole object as returned by
        a read operation."""

        pass

    def hammer_it(self, request_type, url, request_body = {}, 
                content_type="text", accept = 'json'):
        """
        A slim version of simonv3's excellent keep_trying method. Among other
         trimmings, it assumes we can only use v3 of the
         QBO API. It also allows for requests and responses
         in xml OR json. (No xml parsing added yet but the way is paved...)
        """

        if self.session != None:
            session = self.session
        else:
            session = self.create_session()
            self.session = session

        #haven't found an example of when this wouldn't be True, but leaving
        #it for the meantime...
        header_auth = True

        trying       = True
        print_error = False

        tries = 0

        while trying:
            tries += 1


            headers = {
                    'Content-Type': 'application/%s' % content_type,
                    'Accept': 'application/%s' % accept
                }

            r = session.request(request_type, url, header_auth,
                                     self.company_id, headers = headers,
                                     data = request_body)

            if accept == "json":

                if r.status_code == 401:

                    raise Exception('Query object is not authorized to make that request.')

                result = r.json()

                if "Fault" in result and result["Fault"]\
                   ["type"] == "ValidationFault":

                    if self.verbose:

                        print "Fault alert!"

                    trying = False
                    print_error = True


                elif tries >= 6:

                    trying = False

                    if "Fault" in result:
                        print_error = True

                elif "Fault" not in result:

                    #sounds like a success
                    trying = False

                if not trying and print_error:

                    print json.dumps(result, indent=1)

            else:
                raise NotImplementedError("How do I parse a %s response?") \
                    % accept

        return result

    def get_single_object(self, qbbo, pk=None):
        if pk:
            if qbbo not in self._BUSINESS_OBJECTS:
                raise Exception("{0} not in list of QBO Business Objects.\n\
                                Please use one of the following:{1}".format(
                                    qbo, self._BUSINESS_OBJECTS))

            url = self.base_url_v3 + "/company/{0}/{1}/{2}/".format(
                                                            self.company_id, 
                                                            qbbo.lower(),
                                                            pk)

            result = self.hammer_it("GET", url, {}, "text")

            return result
        else:
            return {}

    def query_objects(self, business_object, fields='*', params={}, query_tail = ""):
        """
        Runs a query-type request against the QBOv3 API
        Gives you the option to create an AND-joined query by parameter
            or just pass in a whole query tail
        The parameter dicts should be keyed by parameter name and
            have twp-item tuples for values, which are operator and criterion
        """

        if business_object not in self._BUSINESS_OBJECTS:
            raise Exception("{0} not in list of QBO Business Objects.\n\
                            Please use one of the following: {1}".format(
                                business_object, self._BUSINESS_OBJECTS))

        if isinstance(fields, list):
            fields = ','.join(fields)

        query_string="SELECT {0} FROM {1}".format(fields, business_object)

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
                raise Exception("Unfamiliar property: {0}".format(p[0]))

            query_string+=" WHERE {0} {1} {2}".format(p[0], params[p[0]][0], params[p[0]][1])

            if len(p)>1:
                for i in range(1,len(p)+1):
                    if p[i] not in props:
                        raise Exception("Unfamiliar property: {}".format(p[i]))

                    query_string+=" AND {0} {1} {2}".format(p[i], params[p[i]][0],
                                                     params[p[i]][1])

        elif not query_tail == "":
            if not query_tail[0]==" ":
                query_tail = " "+query_tail
            query_string+=query_tail

        #CAN ONE SESSION USE MULTIPLE COMPANIES?
        #IF NOT, REMOVE THE COMPANY OPTIONALITY
        url = self.base_url_v3 + "/company/{}/query".format(self.company_id)

        #print query_string

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
            raise Exception("{} is not a valid QBO Business\
                    Object.".format(qbbo)) 

        attr_name = qbbo+"s"

        #if we've already populated this list, only redo if told to
        #because, say, we've created another Account or Item or something
        #during the session

        if not hasattr(self,attr_name) or requery:

            if self.verbose:
                print("Caching list of {}s.".format(qbbo))

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
        returns a dict of dicts of ALL the Business Objects of
        each of these types (filtering with params and query_tail)
        """

        object_dicts = {}       #{qbbo:[object_list]}

        for qbbo in qbbo_list:

            if qbbo == "TimeActivity":
                #for whatever reason, this failed with some basic criteria, so
                query_tail = ""

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
    # Below are the convenience-function calls that have dependencies
    # -------------------------------------------------------------

    def quick_report(self, filter_attributes = {}):
        """see report.quick_report.__doc__"""

        return report.quick_report(self, filter_attributes)

    def chart_of_accounts(self, attrs = "strict"):
        """see report.chart_of_accounts"""

        return report.chart_of_accounts(self, attrs)

    def name_list(self):
        """
        see massage.name_list()

        Note that this sets some attributes of the session object!
        """

        return massage.name_list(self)

    def ledgerize(self, transaction, headers=False):
        """see ledgerize.__doc__ in the massage module"""
        
        return massage.ledgerize(transaction, self, headers)

    def ledger_lines(self, qbbo=None, Id=None, line_number=None, headers=False,
                     **kwargs):
        """
        see massage.ledger_lines.__doc__
        Note that this sets some attributes of this session object, including:
         self.ledger_lines_dict (for future reference)
         self.earliest_date, self.latest_date (for efficiency in reporting)
        """

        return massage.ledger_lines(self, qbbo, Id, line_number, headers,
                                    **kwargs)
                    
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


    def gl(self):
        """
        For now, this just returns all the lines (we can get...excludes such
        things as deposits and transfers...thanks, Intuit!)
        """
        
        #the True gives us headers!
        unsorted_gl = self.ledger_lines(None, None, None, True)

        #sort the thing by account THEN by date, obvi

        sorted_gl   = unsorted_gl   #just for now...fix later!

        return sorted_gl

    def pnl(self, period = "YEARLY", start_date="first", end_date="last",
            **kwargs):
        """
        Again, subject to the missing transactions, this tallies things by
        period (which is initially either MONTHLY or YEARLY, but will
        eventually be arbitrary, hopefully)
        """

        #kwargs can include filter strings (to do a pnl of only recent
        #additions, for example)

        return report.pnl(self, period, start_date, end_date, **kwargs)
