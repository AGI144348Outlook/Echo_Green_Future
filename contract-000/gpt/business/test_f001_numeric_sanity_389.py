import unittest
from decimal import Decimal as D
from f001_numeric_sanity_389 import mass_difference_percent, angular_fraction, unit_count_for_tons, summarize

class NumericSanity(unittest.TestCase):
    def test_buyer_denominator(self):
        self.assertEqual(mass_difference_percent('11.4').quantize(D('0.01')), D('20.18'))
    def test_seller_denominator(self):
        self.assertEqual(mass_difference_percent('13.7').quantize(D('0.01')), D('16.79'))
    def test_denominator_matters(self):
        self.assertNotEqual(mass_difference_percent('11.4'), mass_difference_percent('13.7'))
    def test_angular_exact(self):
        self.assertEqual(angular_fraction(), D('49.320'))
    def test_angular_rounding(self):
        self.assertEqual(angular_fraction().quantize(D('0.1')), D('49.3'))
    def test_angle_is_not_exactly_49_3(self):
        self.assertNotEqual(angular_fraction(), D('49.3'))
    def test_metric_ton(self):
        self.assertEqual(unit_count_for_tons('1000000'), D('1000000'))
    def test_us_short_ton(self):
        self.assertEqual(unit_count_for_tons('907184.74'), D('907184.74'))
    def test_uk_long_ton(self):
        self.assertEqual(unit_count_for_tons('1016046.9088'), D('1016046.9088'))
    def test_ton_ambiguity(self):
        self.assertNotEqual(unit_count_for_tons('1000000'), unit_count_for_tons('907184.74'))
    def test_no_unearned_evidence(self):
        self.assertIn('No result proves', summarize()['note'])

if __name__ == '__main__':
    unittest.main()
