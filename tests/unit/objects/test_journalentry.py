import unittest

from quickbooks.objects.journalentry import JournalEntry, JournalEntryLine, JournalEntryLineDetail


class JournalentryTests(unittest.TestCase):
    def test_unicode(self):
        journalentry = JournalEntry()
        journalentry.Adjustment = True

        self.assertEquals(unicode(journalentry), 'True')


class JournalEntryLineTests(unittest.TestCase):
    def test_unicode(self):
        journalentry = JournalEntryLine()
        journalentry.Amount = 100

        self.assertEquals(unicode(journalentry), "100")


class JournalEntryLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        journalentry = JournalEntryLineDetail()
        journalentry.PostingType = "test"

        self.assertEquals(unicode(journalentry), "test")
