import unittest
from unittest.mock import patch
from main_PSX import analyze_symbol

class TestMainPSX(unittest.TestCase):
    def test_analyze_symbol(self):
        symbol = "AAPL"
        analysis_type = "D"
        screener_selection = "PAKISTAN"
        exchange_selection = "PSX"
        BASE_URL_CHARTS = "https://www.tradingview.com/chart/ZMYE714n/?symbol=PSX%3A"
        BASE_URL_FINANCE = "https://www.tradingview.com/symbols/PSX-"
        BASE_URL_TECH = "https://www.tradingview.com/symbols/PSX-"

        result = analyze_symbol(symbol, analysis_type, screener_selection, exchange_selection, BASE_URL_CHARTS, BASE_URL_FINANCE, BASE_URL_TECH)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 18)
        self.assertEqual(result[0], symbol)
        self.assertIsInstance(result[1], dict)
        self.assertIsInstance(result[2], float)
        self.assertIsInstance(result[3], str)
        self.assertIsInstance(result[4], str)
        self.assertIsInstance(result[5], str)
        self.assertIsInstance(result[6], int)
        self.assertIsInstance(result[7], float)
        self.assertIsInstance(result[8], float)
        self.assertIsInstance(result[9], float)
        self.assertIsInstance(result[10], float)
        self.assertIsInstance(result[11], float)
        self.assertIsInstance(result[12], float)
        self.assertIsInstance(result[13], float)
        self.assertEqual(result[14], BASE_URL_CHARTS)
        self.assertEqual(result[15], BASE_URL_FINANCE)
        self.assertEqual(result[16], BASE_URL_TECH)

if __name__ == '__main__':
    unittest.main()