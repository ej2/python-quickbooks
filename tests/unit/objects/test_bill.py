import unittest

from quickbooks import QuickBooks
from quickbooks.objects.bill import Bill


class BillTests(unittest.TestCase):
    def test_unicode(self):
        bill = Bill()
        bill.Balance = 1000

        self.assertEqual(str(bill), "1000")

    def test_to_LinkedTxn(self):
        bill = Bill()
        bill.Id = 10

        linked_txn = bill.to_linked_txn()

        self.assertEqual(linked_txn.TxnId, bill.Id)
        self.assertEqual(linked_txn.TxnType, "Bill")
        self.assertEqual(linked_txn.TxnLineId, 1)

    def test_valid_object_name(self):
        obj = Bill()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)

    def test_to_ref(self):
        bill = Bill()
        bill.DocNumber = "test"
        bill.Id = 100

        ref = bill.to_ref()

        self.assertEqual(ref.name, "test")
        self.assertEqual(ref.type, "Bill")
        self.assertEqual(ref.value, 100)

