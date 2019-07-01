import unittest
try:
	from mock import patch
except ImportError:
	from unittest.mock import patch
from quickbooks.cdc import change_data_capture
from quickbooks.objects import Invoice, Customer
from quickbooks import QuickBooks
from datetime import datetime

class ChangeDataCaptureTest(unittest.TestCase):

	def setUp(self):
		self.qb_client = QuickBooks(
			sandbox=True,
			consumer_key="update_consumer_key",
			consumer_secret="update_consumer_secret",
			access_token="update_access_token",
			access_token_secret="update_access_token_secret",
			company_id="update_company_id",
			callback_url="update_callback_url"
		)

		self.cdc_json_response = {
			"CDCResponse": [
				{
					"QueryResponse": [
						{
							"Customer": [
								{
									"Id": 1,
									"DisplayName": "TestCustomer",
									"Job": False,
									"Balance": 0
								}
							],
							"startPosition": 1,
							"maxResults": 1
						},
						{
							"Invoice": [
								{
									"DocNumber": "12344",
									"TxnDate": "2017-01-01",
									"Line": [
										{
											"Id": 1
										},
										{
											"Id": 2
										}
									]
								},
								{
									"DocNumber": "12345",
									"TxnDate": "2017-01-01",
									"Line": [
										{
											"Id": 1
										},
										{
											"Id": 2
										}
									]
								},
							],
							"startPosition": 1,
							"maxResults": 2
						}
					]
				}
			],
			"time": "2016-01-01T00:00:00"
		}

		self.cdc_empty_json_response = {
			"CDCResponse": [
				{
					"QueryResponse": [
						{}
					]
				}
			],
			"time": "2019-03-13T10:24:05.179-07:00"
		}


	@patch('quickbooks.client.QuickBooks.make_request')
	def test_change_data_capture(self, make_request):
		make_request.return_value = self.cdc_json_response.copy()
		cdc_response = change_data_capture([Invoice, Customer], "2017-01-01T00:00:00")
		self.assertEquals(1, len(cdc_response.Customer))
		self.assertEquals(2, len(cdc_response.Invoice))


	@patch('quickbooks.client.QuickBooks.make_request')
	def test_change_data_capture_with_timestamp(self, make_request):
		make_request.return_value = self.cdc_json_response.copy()
		cdc_response_with_datetime = change_data_capture([Invoice, Customer], datetime(2017, 1, 1, 0, 0, 0))
		self.assertEquals(1, len(cdc_response_with_datetime.Customer))
		self.assertEquals(2, len(cdc_response_with_datetime.Invoice))

	@patch('quickbooks.client.QuickBooks.make_request')
	def test_change_data_capture_with_empty_response(self, make_request):
		make_request.return_value = self.cdc_empty_json_response.copy()
		cdc_response = change_data_capture([Invoice, Customer], datetime(2017, 1, 1, 0, 0, 0))

		self.assertFalse(hasattr(cdc_response, 'Customer'))
		self.assertFalse(hasattr(cdc_response, 'Invoice'))
