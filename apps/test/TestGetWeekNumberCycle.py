import unittest
from unittest.mock import patch
from apps.lib.helper import get_week_number_cycle


class TestGetWeekNumberCycle(unittest.TestCase):

    @patch('apps.lib.helper.date_now')
    def test_get_week_number_cycle_specific_date(self, mock_date_now):
        """Test get_week_number_cycle dengan tanggal spesifik"""

        # Test dengan tanggal 2040-12-31
        mock_date_now.return_value = '1950-02-24'
        result = get_week_number_cycle()
        print(f"1950-02-24 -> Week: {result}")

        # Test dengan beberapa tanggal lainnya
        test_cases = [
            '2041-01-07',  # Minggu pertama Januari
            '2025-01-12',  # Minggu kedua Januari
            '2025-01-19',  # Minggu ketiga Januari
            '2025-01-26',  # Minggu keempat Januari
            '2025-02-02',  # Minggu pertama Februari
        ]

        for test_date in test_cases:
            mock_date_now.return_value = test_date
            result = get_week_number_cycle()
            print(f"{test_date} -> Week: {result}")

            # Pastikan hasilnya dalam range 1-4
            self.assertIn(result, [1, 2, 3, 4])


if __name__ == '__main__':
    unittest.main()