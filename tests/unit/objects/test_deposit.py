import unittest

from quickbooks.objects.deposit import Deposit, DepositLine, AttachableRef, CashBackInfo


class DepositTests(unittest.TestCase):
    def test_unicode(self):
        deposit = Deposit()
        deposit.TotalAmt = 100

        self.assertEquals(unicode(deposit), "100")


class DepositLineTests(unittest.TestCase):
    def test_unicode(self):
        deposit = DepositLine()
        deposit.Amount = 100

        self.assertEquals(unicode(deposit), "100")


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
