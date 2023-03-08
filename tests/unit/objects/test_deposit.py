import unittest

from quickbooks import QuickBooks
from quickbooks.objects.deposit import Deposit, DepositLine, CashBackInfo, DepositLineDetail


class DepositTests(unittest.TestCase):
    def test_unicode(self):
        deposit = Deposit()
        deposit.TotalAmt = 100

        self.assertEqual(str(deposit), "100")

    def test_valid_object_name(self):
        obj = Deposit()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)


class DepositLineTests(unittest.TestCase):
    def test_unicode(self):
        deposit = DepositLine()
        deposit.Amount = 100

        self.assertEqual(str(deposit), "100")


class CashBackInfoTests(unittest.TestCase):
    def test_init(self):
        cash_back_info = CashBackInfo()

        self.assertEqual(cash_back_info.Amount, 0)
        self.assertEqual(cash_back_info.Memo, "")
        self.assertEqual(cash_back_info.AccountRef, None)


class DepositLineDetailTests(unittest.TestCase):
    def test_init(self):
        detail = DepositLineDetail()

        self.assertEqual(detail.Entity, None)
        self.assertEqual(detail.ClassRef, None)
        self.assertEqual(detail.AccountRef, None)
        self.assertEqual(detail.PaymentMethodRef, None)
        self.assertEqual(detail.CheckNum, "")
        self.assertEqual(detail.TxnType, None)
