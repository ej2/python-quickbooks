import unittest

from quickbooks import QuickBooks
from quickbooks.objects.bill import Bill


class BillTests(unittest.TestCase):
    def test_unicode(self):
        bill = Bill()
        bill.Balance = 1000

        self.assertEquals(str(bill), "1000")

    def test_to_LinkedTxn(self):
        bill = Bill()
        bill.Id = 10

        linked_txn = bill.to_linked_txn()

        self.assertEquals(linked_txn.TxnId, bill.Id)
        self.assertEquals(linked_txn.TxnType, "Bill")
        self.assertEquals(linked_txn.TxnLineId, 1)

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

        self.assertEquals(ref.name, "test")
        self.assertEquals(ref.type, "Bill")
        self.assertEquals(ref.value, 100)

