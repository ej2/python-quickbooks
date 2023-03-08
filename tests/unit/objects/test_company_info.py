import unittest

from quickbooks import QuickBooks
from quickbooks.objects.company_info import CompanyInfo


class CompanyInfoTests(unittest.TestCase):
    def test_unicode(self):
        company_info = CompanyInfo()
        company_info.CompanyName = "test"

        self.assertEqual(str(company_info), "test")

    def test_to_ref(self):
        company_info = CompanyInfo()
        company_info.CompanyName = "test"
        company_info.Id = 100

        ref = company_info.to_ref()

        self.assertEqual(ref.name, "test")
        self.assertEqual(ref.type, "CompanyInfo")
        self.assertEqual(ref.value, 100)
