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

        self.assertEquals(preferences.Id, "1")
        self.assertEquals(preferences.AccountingInfoPrefs.TaxYearMonth, "January")
        self.assertEquals(preferences.ProductAndServicesPrefs.ForPurchase, True)
        self.assertEquals(preferences.VendorAndPurchasesPrefs.BillableExpenseTracking, True)
        self.assertEquals(preferences.TimeTrackingPrefs.WorkWeekStartDate, "Monday")
        self.assertEquals(preferences.OtherPrefs.NameValue[0].Name, "SalesFormsPrefs.DefaultCustomerMessage")

    def test_update(self):
        preferences = Preferences.get(qb=self.qb_client)

        subject = datetime.now().strftime('%d%H%M%S')
        preferences.EmailMessagesPrefs.EstimateMessage.Subject = subject
        preferences.save(qb=self.qb_client)

        preferences_updated = Preferences.get(qb=self.qb_client)
        self.assertEquals(preferences_updated.EmailMessagesPrefs.EstimateMessage.Subject, subject)
