import unittest
from mock import patch

from quickbooks.objects.base import PhoneNumber
from quickbooks.objects.department import Department
from quickbooks.objects.salesreceipt import SalesReceipt


class ToJsonMixinTest(unittest.TestCase):
    def test_to_json(self):
        phone = PhoneNumber()
        phone.FreeFormNumber = "555-555-5555"

        json = phone.to_json()

        self.assertEquals(json, '{\n    "FreeFormNumber": "555-555-5555"\n}')


class ListMixinTest(unittest.TestCase):
    @patch('quickbooks.mixins.ListMixin.where')
    def test_all(self, where):
        Department.all()
        where.assert_called_once_with('', max_results=100, start_position='')

    @patch('quickbooks.mixins.ListMixin.where')
    def test_filter(self, where):
        Department.filter(max_results=25, start_position='1', Active=True)
        where.assert_called_once_with("Active = True", max_results=25, start_position='1')

    @patch('quickbooks.mixins.ListMixin.query')
    def test_where(self, query):
        Department.where("Active=True", 1, 10)
        query.assert_called_once_with("SELECT * FROM Department WHERE Active=True STARTPOSITION 1 MAXRESULTS 10")

    @patch('quickbooks.mixins.QuickBooks.query')
    def test_query(self, query):
        select = "SELECT * FROM Department WHERE Active=True"
        Department.query(select)
        query.assert_called_once_with(select)

    @patch('quickbooks.mixins.ListMixin.where')
    def test_choose(self, where):
        Department.choose(['name1', 'name2'], field="Name")
        where.assert_called_once_with("Name in ('name1', 'name2')")


class ReadMixinTest(unittest.TestCase):
    @patch('quickbooks.mixins.QuickBooks.get_single_object')
    def test_get(self, get_single_object):
        Department.get(1)
        get_single_object.assert_called_once_with("Department", pk=1)


class UpdateMixinTest(unittest.TestCase):
    @patch('quickbooks.mixins.QuickBooks.create_object')
    def test_save_create(self, create_object):
        department = Department()
        department.save()
        create_object.assert_called_once_with("Department", department.to_json())

    @patch('quickbooks.mixins.QuickBooks.update_object')
    def test_save_update(self, update_object):
        department = Department()
        department.Id = 1
        json = department.to_json()

        department.save()
        update_object.assert_called_once_with("Department", json)


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
