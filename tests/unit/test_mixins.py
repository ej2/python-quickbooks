import unittest
from mock import patch, Mock

from quickbooks import client

from quickbooks.objects.base import PhoneNumber, QuickbooksBaseObject
from quickbooks.objects.department import Department
from quickbooks.objects.journalentry import JournalEntry, JournalEntryLine
from quickbooks.objects.salesreceipt import SalesReceipt


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


class ListMixinTest(unittest.TestCase):
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
    @patch('quickbooks.client.QuickBooks.download_pdf')
    def test_download_invoice(self, download_pdf):
        receipt = SalesReceipt()
        receipt.Id = 1

        receipt.download_pdf()
        download_pdf.assert_called_once_with('SalesReceipt', 1)

    def test_download_missing_id(self):
        from quickbooks.exceptions import QuickbooksException

        receipt = SalesReceipt()
        self.assertRaises(QuickbooksException, receipt.download_pdf)
