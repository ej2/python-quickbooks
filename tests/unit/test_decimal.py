from decimal import Decimal
import unittest
from quickbooks.objects.bill import Bill
from quickbooks.objects.detailline import DetailLine


class DecimalTestCase(unittest.TestCase):
    def test_bill_with_decimal_amount(self):
        """Test that a Bill with decimal line amounts can be converted to JSON without errors"""
        bill = Bill()
        line = DetailLine()
        line.Amount = Decimal('42.42')
        line.DetailType = "AccountBasedExpenseLineDetail"
        
        bill.Line.append(line)
        
        # This should not raise any exceptions
        json_data = bill.to_json()
        
        # Verify the amount was converted correctly
        self.assertIn('"Amount": "42.42"', json_data)
