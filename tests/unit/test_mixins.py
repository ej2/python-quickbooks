import unittest
from mock import patch

from quickbooks.objects.base import PhoneNumber
from quickbooks.objects.department import Department


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
        Department.where("Active=True")
        query.assert_called_once_with("select * from Department WHERE Active=True")

    @patch('quickbooks.mixins.QuickBooks.query')
    def test_query(self, query):
        select = "select * from Department WHERE Active=True"
        Department.query(select)
        query.assert_called_once_with(select)


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
