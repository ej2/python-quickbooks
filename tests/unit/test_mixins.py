import os
import unittest

from quickbooks.objects import Bill, Invoice
from quickbooks.auth import Oauth1SessionManager

try:
    from mock import patch
except ImportError:
    from unittest.mock import patch

from quickbooks import client

from quickbooks.objects.base import PhoneNumber, QuickbooksBaseObject
from quickbooks.objects.department import Department
from quickbooks.objects.journalentry import JournalEntry, JournalEntryLine
from quickbooks.objects.salesreceipt import SalesReceipt
from quickbooks.mixins import ObjectListMixin


class ToJsonMixinTest(unittest.TestCase):
    def test_to_json(self):
        phone = PhoneNumber()
        phone.FreeFormNumber = "555-555-5555"

        json = phone.to_json()

        self.assertEquals(json, '{\n    "FreeFormNumber": "555-555-5555"\n}')


class FromJsonMixinTest(unittest.TestCase):
    def setUp(self):
        self.json_data = {
            'DocNumber': '123',
            'TotalAmt': 100,
            'Line': [
                {
                    "Id": "0",
                    "Description": "Test",
                    "Amount": 25.54,
                    "DetailType": "JournalEntryLineDetail",
                    "JournalEntryLineDetail": {
                        "PostingType": "Debit",
                    }
                },
            ],
        }

    def test_from_json(self):
        entry = JournalEntry()
        new_obj = entry.from_json(self.json_data)

        self.assertEquals(type(new_obj), JournalEntry)
        self.assertEquals(new_obj.DocNumber, "123")
        self.assertEquals(new_obj.TotalAmt, 100)

        line = new_obj.Line[0]
        self.assertEquals(type(line), JournalEntryLine)
        self.assertEquals(line.Description, "Test")
        self.assertEquals(line.Amount, 25.54)
        self.assertEquals(line.DetailType, "JournalEntryLineDetail")
        self.assertEquals(line.JournalEntryLineDetail.PostingType, "Debit")

    def test_from_json_missing_detail_object(self):
        test_obj = QuickbooksBaseObject()

        new_obj = test_obj.from_json(self.json_data)

        self.assertEquals(type(new_obj), QuickbooksBaseObject)
        self.assertEquals(new_obj.DocNumber, "123")
        self.assertEquals(new_obj.TotalAmt, 100)


class ToDictMixinTest(unittest.TestCase):
    def test_to_dict(self):
        json_data = {
            'DocNumber': '123',
            'TotalAmt': 100,
            'Line': [
                {
                    "Id": "0",
                    "Description": "Test",
                    "Amount": 25.54,
                    "DetailType": "JournalEntryLineDetail",
                    "JournalEntryLineDetail": {
                        "PostingType": "Debit",
                    }
                },
            ],
        }

        entry = JournalEntry.from_json(json_data)
        expected = {
            'DocNumber': '123',
            'SyncToken': 0,
            'domain': 'QBO',
            'TxnDate': '',
            'TotalAmt': 100,
            'ExchangeRate': 1,
            'CurrencyRef': None,
            'PrivateNote': '',
            'sparse': False,
            'Line': [{
                'LinkedTxn': [],
                'Description': 'Test',
                'JournalEntryLineDetail': {
                    'TaxAmount': 0,
                    'Entity': None,
                    'DepartmentRef': None,
                    'TaxCodeRef': None,
                    'BillableStatus': '',
                    'TaxApplicableOn': 'Sales',
                    'PostingType': 'Debit',
                    'AccountRef': None,
                    'ClassRef': None,
                },
                'DetailType': 'JournalEntryLineDetail',
                'LineNum': 0,
                'Amount': 25.54,
                'CustomField': [],
                'Id': '0',
            }],
            'Adjustment': False,
            'Id': None,
            'TxnTaxDetail': None,
        }

        self.assertEquals(expected, entry.to_dict())


class ListMixinTest(unittest.TestCase):
    def setUp(self):
        self.session_manager = Oauth1SessionManager(
            sandbox=True,
            consumer_key="update_consumer_key",
            consumer_secret="update_consumer_secret",
            access_token="update_access_token",
            access_token_secret="update_access_token_secret",
        )

        self.qb_client = client.QuickBooks(
            session_manager=self.session_manager,
            sandbox=True,
            company_id="COMPANY_ID"
        )

    @patch('quickbooks.mixins.ListMixin.where')
    def test_all(self, where):
        Department.all()
        where.assert_called_once_with('', max_results=100, start_position='', qb=None)

    def test_all_with_qb(self):
        with patch.object(self.qb_client, 'query') as query:
            Department.all(qb=self.qb_client)
            self.assertTrue(query.called)

    @patch('quickbooks.mixins.ListMixin.where')
    def test_filter(self, where):
        Department.filter(max_results=25, start_position='1', Active=True)
        where.assert_called_once_with("Active = True", max_results=25, start_position='1', qb=None)

    def test_filter_with_qb(self):
        with patch.object(self.qb_client, 'query') as query:
            Department.filter(Active=True, qb=self.qb_client)
            self.assertTrue(query.called)

    @patch('quickbooks.mixins.ListMixin.query')
    def test_where(self, query):
        Department.where("Active=True", 1, 10)
        query.assert_called_once_with("SELECT * FROM Department WHERE Active=True STARTPOSITION 1 MAXRESULTS 10",
                                      qb=None)

    def test_where_with_qb(self):
        with patch.object(self.qb_client, 'query') as query:
            Department.where("Active=True", 1, 10, qb=self.qb_client)
            self.assertTrue(query.called)

    @patch('quickbooks.mixins.QuickBooks.query')
    def test_query(self, query):
        select = "SELECT * FROM Department WHERE Active=True"
        Department.query(select)
        query.assert_called_once_with(select)

    def test_query_with_qb(self):
        with patch.object(self.qb_client, 'query') as query:
            select = "SELECT * FROM Department WHERE Active=True"
            Department.query(select, qb=self.qb_client)
            self.assertTrue(query.called)

    @patch('quickbooks.mixins.ListMixin.where')
    def test_choose(self, where):
        Department.choose(['name1', 'name2'], field="Name")
        where.assert_called_once_with("Name in ('name1', 'name2')", qb=None)

    def test_choose_with_qb(self):
        with patch.object(self.qb_client, 'query') as query:
            Department.choose(['name1', 'name2'], field="Name", qb=self.qb_client)
            self.assertTrue(query.called)

    @patch('quickbooks.mixins.QuickBooks.query')
    def test_count(self, query):
        count = Department.count(where_clause="Active=True", qb=self.qb_client)
        query.assert_called_once_with("SELECT COUNT(*) FROM Department WHERE Active=True")


class ReadMixinTest(unittest.TestCase):
    def setUp(self):
        self.qb_client = client.QuickBooks(
            sandbox=True,
            consumer_key="update_consumer_key",
            consumer_secret="update_consumer_secret",
            access_token="update_access_token",
            access_token_secret="update_access_token_secret",
            company_id="update_company_id",
            callback_url="update_callback_url"
        )

    @patch('quickbooks.mixins.QuickBooks.get_single_object')
    def test_get(self, get_single_object):
        Department.get(1)
        get_single_object.assert_called_once_with("Department", pk=1)

    def test_get_with_qb(self):
        with patch.object(self.qb_client, 'get_single_object') as get_single_object:
            Department.get(1, qb=self.qb_client)
            self.assertTrue(get_single_object.called)


class UpdateMixinTest(unittest.TestCase):
    def setUp(self):
        self.qb_client = client.QuickBooks(
            sandbox=True,
            consumer_key="update_consumer_key",
            consumer_secret="update_consumer_secret",
            access_token="update_access_token",
            access_token_secret="update_access_token_secret",
            company_id="update_company_id",
            callback_url="update_callback_url"
        )

    @patch('quickbooks.mixins.QuickBooks.create_object')
    def test_save_create(self, create_object):
        department = Department()
        department.save(qb=self.qb_client)
        create_object.assert_called_once_with("Department", department.to_json())

    def test_save_create_with_qb(self):
        with patch.object(self.qb_client, 'create_object') as create_object:
            department = Department()
            department.save(qb=self.qb_client)
            self.assertTrue(create_object.called)

    @patch('quickbooks.mixins.QuickBooks.update_object')
    def test_save_update(self, update_object):
        department = Department()
        department.Id = 1
        json = department.to_json()

        department.save(qb=self.qb_client)
        update_object.assert_called_once_with("Department", json)

    def test_save_update_with_qb(self):
        with patch.object(self.qb_client, 'update_object') as update_object:
            department = Department()
            department.Id = 1
            json = department.to_json()

            department.save(qb=self.qb_client)
            self.assertTrue(update_object.called)


class DownloadPdfTest(unittest.TestCase):
    def setUp(self):
        self.qb_client = client.QuickBooks(
            sandbox=True,
            consumer_key="update_consumer_key",
            consumer_secret="update_consumer_secret",
            access_token="update_access_token",
            access_token_secret="update_access_token_secret",
            company_id="update_company_id",
            callback_url="update_callback_url"
        )

    @patch('quickbooks.client.QuickBooks.download_pdf')
    def test_download_invoice(self, download_pdf):
        receipt = SalesReceipt()
        receipt.Id = "1"

        receipt.download_pdf(self.qb_client)
        download_pdf.assert_called_once_with('SalesReceipt', "1")

    def test_download_missing_id(self):
        from quickbooks.exceptions import QuickbooksException

        receipt = SalesReceipt()
        self.assertRaises(QuickbooksException, receipt.download_pdf)


class ObjectListTest(unittest.TestCase):

    def setUp(self):
        class TestSubclass(ObjectListMixin):

            def __init__(self, obj_list):
                super(TestSubclass, self).__init__()
                self._object_list = obj_list

        self.TestSubclass = TestSubclass

    def test_object_list_mixin_with_primitives(self):

        test_primitive_list = [1, 2, 3]
        test_subclass_primitive_obj = self.TestSubclass(test_primitive_list)
        self.assertEquals(test_primitive_list, test_subclass_primitive_obj[:])

        for index in range(0, len(test_subclass_primitive_obj)):
            self.assertEquals(test_primitive_list[index], test_subclass_primitive_obj[index])

        for prim in test_subclass_primitive_obj:
            self.assertEquals(True, prim in test_subclass_primitive_obj)

        self.assertEquals(3, test_subclass_primitive_obj.pop())
        test_subclass_primitive_obj.append(4)
        self.assertEquals([1, 2, 4], test_subclass_primitive_obj[:])

        test_subclass_primitive_obj[0] = 5
        self.assertEquals([5, 2, 4], test_subclass_primitive_obj[:])

        del test_subclass_primitive_obj[0]
        self.assertEquals([2, 4], test_subclass_primitive_obj[:])

        self.assertEquals([4, 2], list(reversed(test_subclass_primitive_obj)))

    def test_object_list_mixin_with_qb_objects(self):

        pn1, pn2, pn3, pn4, pn5 = PhoneNumber(), PhoneNumber(), PhoneNumber(), PhoneNumber(), PhoneNumber()
        test_object_list = [pn1, pn2, pn3]
        test_subclass_object_obj = self.TestSubclass(test_object_list)
        self.assertEquals(test_object_list, test_subclass_object_obj[:])

        for index in range (0, len(test_subclass_object_obj)):
            self.assertEquals(test_object_list[index], test_subclass_object_obj[index])

        for obj in test_subclass_object_obj:
            self.assertEquals(True, obj in test_subclass_object_obj)

        self.assertEquals(pn3, test_subclass_object_obj.pop())
        test_subclass_object_obj.append(pn4)
        self.assertEquals([pn1, pn2, pn4], test_subclass_object_obj[:])

        test_subclass_object_obj[0] = pn5
        self.assertEquals([pn5, pn2, pn4], test_subclass_object_obj[:])

        del test_subclass_object_obj[0]
        self.assertEquals([pn2, pn4], test_subclass_object_obj[:])

        self.assertEquals([pn4, pn2], list(reversed(test_subclass_object_obj)))


class DeleteMixinTest(unittest.TestCase):
    def setUp(self):
        self.qb_client = client.QuickBooks(
            sandbox=True,
            consumer_key="update_consumer_key",
            consumer_secret="update_consumer_secret",
            access_token="update_access_token",
            access_token_secret="update_access_token_secret",
            company_id="update_company_id",
            callback_url="update_callback_url"
        )

    def test_delete_unsaved_exception(self):
        from quickbooks.exceptions import QuickbooksException

        bill = Bill()
        self.assertRaises(QuickbooksException, bill.delete, qb=self.qb_client)

    @patch('quickbooks.mixins.QuickBooks.delete_object')
    def test_delete(self, delete_object):
        bill = Bill()
        bill.Id = 1
        bill.delete(qb=self.qb_client)

        self.assertTrue(delete_object.called)


class SendMixinTest(unittest.TestCase):
    def setUp(self):
        self.qb_client = client.QuickBooks(
            sandbox=True,
            consumer_key="update_consumer_key",
            consumer_secret="update_consumer_secret",
            access_token="update_access_token",
            access_token_secret="update_access_token_secret",
            company_id="update_company_id",
            callback_url="update_callback_url"
        )

    @patch('quickbooks.mixins.QuickBooks.misc_operation')
    def test_send(self, mock_misc_op):
        invoice = Invoice()
        invoice.Id = 2
        invoice.send(qb=self.qb_client)

        mock_misc_op.assert_called_with("invoice/2/send", None, 'application/octet-stream')

    @patch('quickbooks.mixins.QuickBooks.misc_operation')
    def test_send_with_send_to_email(self, mock_misc_op):
        invoice = Invoice()
        invoice.Id = 2
        invoice.send(qb=self.qb_client, send_to="test@email.com")

        mock_misc_op.assert_called_with("invoice/2/send?sendTo=test@email.com", None, 'application/octet-stream')
