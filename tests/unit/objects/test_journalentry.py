import unittest

from quickbooks import QuickBooks
from quickbooks.objects.journalentry import JournalEntry, JournalEntryLine, JournalEntryLineDetail, Entity, \
    DescriptionLineDetail, DescriptionOnlyLine


class JournalentryTests(unittest.TestCase):
    def test_unicode(self):
        journalentry = JournalEntry()
        journalentry.TotalAmt = 1000

        self.assertEquals(str(journalentry), '1000')

    def test_valid_object_name(self):
        obj = JournalEntry()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)


class JournalEntryLineTests(unittest.TestCase):
    def test_init(self):
        journalentry = JournalEntryLine()

        self.assertEquals(journalentry.DetailType, "JournalEntryLineDetail")
        self.assertEquals(journalentry.JournalEntryLineDetail, None)


class JournalEntryLineDetailTests(unittest.TestCase):
    def test_init(self):
        journalentry = JournalEntryLineDetail()

        self.assertEquals(journalentry.PostingType, "")
        self.assertEquals(journalentry.TaxApplicableOn, "Sales")
        self.assertEquals(journalentry.TaxAmount, 0)
        self.assertEquals(journalentry.BillableStatus, "")
        self.assertEquals(journalentry.Entity, None)
        self.assertEquals(journalentry.AccountRef, None)
        self.assertEquals(journalentry.ClassRef, None)
        self.assertEquals(journalentry.DepartmentRef, None)
        self.assertEquals(journalentry.TaxCodeRef, None)


class EntityTests(unittest.TestCase):
    def test_init(self):
        entity = Entity()

        self.assertEquals(entity.Type, "")
        self.assertEquals(entity.EntityRef, None)


class DescriptionLineDetailTests(unittest.TestCase):
    def test_init(self):
        detail = DescriptionLineDetail()

        self.assertEquals(detail.ServiceDate, "")


class DescriptionOnlyLineTests(unittest.TestCase):
    def test_init(self):
        line = DescriptionOnlyLine()

        self.assertEquals(line.DetailType, "DescriptionOnly")
