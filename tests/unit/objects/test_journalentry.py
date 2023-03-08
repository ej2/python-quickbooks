import unittest

from quickbooks import QuickBooks
from quickbooks.objects.journalentry import JournalEntry, JournalEntryLine, JournalEntryLineDetail, Entity


class JournalentryTests(unittest.TestCase):
    def test_unicode(self):
        journalentry = JournalEntry()
        journalentry.TotalAmt = 1000

        self.assertEqual(str(journalentry), '1000')

    def test_valid_object_name(self):
        obj = JournalEntry()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)


class JournalEntryLineTests(unittest.TestCase):
    def test_init(self):
        journalentry = JournalEntryLine()

        self.assertEqual(journalentry.DetailType, "JournalEntryLineDetail")
        self.assertEqual(journalentry.JournalEntryLineDetail, None)


class JournalEntryLineDetailTests(unittest.TestCase):
    def test_init(self):
        journalentry = JournalEntryLineDetail()

        self.assertEqual(journalentry.PostingType, "")
        self.assertEqual(journalentry.TaxApplicableOn, "Sales")
        self.assertEqual(journalentry.TaxAmount, 0)
        self.assertEqual(journalentry.BillableStatus, None)
        self.assertEqual(journalentry.Entity, None)
        self.assertEqual(journalentry.AccountRef, None)
        self.assertEqual(journalentry.ClassRef, None)
        self.assertEqual(journalentry.DepartmentRef, None)
        self.assertEqual(journalentry.TaxCodeRef, None)


class EntityTests(unittest.TestCase):
    def test_init(self):
        entity = Entity()

        self.assertEqual(entity.Type, "")
        self.assertEqual(entity.EntityRef, None)
