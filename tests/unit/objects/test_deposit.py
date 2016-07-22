import unittest

from quickbooks import QuickBooks
from quickbooks.objects.deposit import Deposit, DepositLine, AttachableRef, CashBackInfo, DepositLineDetail


class DepositTests(unittest.TestCase):
    def test_unicode(self):
        deposit = Deposit()
        deposit.TotalAmt = 100

        self.assertEquals(str(deposit), "100")

    def test_valid_object_name(self):
        obj = Deposit()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)


class DepositLineTests(unittest.TestCase):
    def test_unicode(self):
        deposit = DepositLine()
        deposit.Amount = 100

        self.assertEquals(str(deposit), "100")


class AttachableRefTests(unittest.TestCase):
    def test_init(self):
        attachable_ref = AttachableRef()

        self.assertEquals(attachable_ref.LineInfo, "")
        self.assertFalse(attachable_ref.IncludeOnSend)
        self.assertFalse(attachable_ref.Inactive)
        self.assertFalse(attachable_ref.NoRefOnly)
        self.assertEquals(attachable_ref.EntityRef, None)


class CashBackInfoTests(unittest.TestCase):
    def test_init(self):
        cash_back_info = CashBackInfo()

        self.assertEquals(cash_back_info.Amount, 0)
        self.assertEquals(cash_back_info.Memo, "")
        self.assertEquals(cash_back_info.AccountRef, None)


class DepositLineDetailTests(unittest.TestCase):
    def test_init(self):
        detail = DepositLineDetail()

        self.assertEquals(detail.Entity, None)
        self.assertEquals(detail.ClassRef, None)
        self.assertEquals(detail.AccountRef, None)
        self.assertEquals(detail.PaymentMethodRef, None)
        self.assertEquals(detail.CheckNum, "")
        self.assertEquals(detail.TxnType, None)
