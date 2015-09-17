import unittest

from quickbooks.objects.term import Term, AttachableRef


class TermTests(unittest.TestCase):
    def test_unicode(self):
        term = Term()
        term.Name = "test"

        self.assertEquals(unicode(term), "test")


class AttachableRefTests(unittest.TestCase):
    def test_init(self):
        attachable = AttachableRef()
        attachable.Name = "test"

        self.assertEquals(attachable.LineInfo, "")
        self.assertEquals(attachable.IncludeOnSend, False)
        self.assertEquals(attachable.Inactive, False)
        self.assertEquals(attachable.NoRefOnly, False)
        self.assertEquals(attachable.EntityRef, None)
