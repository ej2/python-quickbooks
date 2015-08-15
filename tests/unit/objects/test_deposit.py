import unittest

from quickbooks.objects.deposit import Deposit, DepositLine


class DepositTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_unicode(self):
        deposit = Deposit()
        deposit.TotalAmt = 100

        self.assertEquals(deposit.__unicode__(), 100)


class DepositLineTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_unicode(self):
        deposit = DepositLine()
        deposit.Amount = 100

        self.assertEquals(deposit.__unicode__(), 100)