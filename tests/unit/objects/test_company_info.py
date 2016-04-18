import unittest

from quickbooks.objects.company_info import CompanyInfo


class CompanyInfoTests(unittest.TestCase):
    def test_unicode(self):
        company_info = CompanyInfo()
        company_info.CompanyName = "test"

        self.assertEquals(str(company_info), "test")

    def test_to_ref(self):
        company_info = CompanyInfo()
        company_info.CompanyName = "test"
        company_info.Id = 100

        ref = company_info.to_ref()

        self.assertEquals(ref.name, "test")
        self.assertEquals(ref.type, "CompanyInfo")
        self.assertEquals(ref.value, 100)
