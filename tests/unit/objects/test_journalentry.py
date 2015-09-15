import unittest

from quickbooks.objects.journalentry import JournalEntry, JournalEntryLine, JournalEntryLineDetail


class JournalentryTests(unittest.TestCase):
    def test_unicode(self):
        journalentry = JournalEntry()
        journalentry.TotalAmt = 1000

        self.assertEquals(unicode(journalentry), '1000')


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
