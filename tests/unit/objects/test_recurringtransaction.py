import unittest

from quickbooks import QuickBooks
from quickbooks.objects.recurringtransaction import RecurringTransaction

class RecurringTransactionTests(unittest.TestCase):
    def test_valid_object_name(self):
        obj = RecurringTransaction()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)