from datetime import datetime
from quickbooks.objects.preferences import Preferences
from tests.integration.test_base import QuickbooksTestCase


class PreferencesTest(QuickbooksTestCase):
    def setUp(self):
        super(PreferencesTest, self).setUp()

        self.account_number = datetime.now().strftime('%d%H%M')
        self.name = "Test Account {0}".format(self.account_number)

    def test_get(self):
        preferences = Preferences.get(qb=self.qb_client)

        self.assertEqual(preferences.Id, "1")
        self.assertEqual(preferences.AccountingInfoPrefs.TaxYearMonth, "January")
        self.assertEqual(preferences.ProductAndServicesPrefs.ForPurchase, True)
        self.assertEqual(preferences.VendorAndPurchasesPrefs.BillableExpenseTracking, True)
        self.assertEqual(preferences.TimeTrackingPrefs.WorkWeekStartDate, "Monday")
        self.assertEqual(preferences.OtherPrefs.NameValue[0].Name, "SalesFormsPrefs.DefaultCustomerMessage")

    def test_update(self):
        preferences = Preferences.get(qb=self.qb_client)

        subject = datetime.now().strftime('%d%H%M%S')
        preferences.EmailMessagesPrefs.EstimateMessage.Subject = subject
        preferences.save(qb=self.qb_client)

        preferences_updated = Preferences.get(qb=self.qb_client)
        self.assertEqual(preferences_updated.EmailMessagesPrefs.EstimateMessage.Subject, subject)
