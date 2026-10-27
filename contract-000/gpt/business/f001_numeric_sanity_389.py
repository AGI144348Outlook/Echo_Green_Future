#!/usr/bin/env python3
"""F-001 Run389: bounded arithmetic only, NOT evidence or editorial approval.
Source references: The-TAM-protocol @ d46456a, README#S24,
The Color Dyed and Dental Records#S14, Collective#S90/#S128, Article10#S5.
No files written, no network, no claims statuses changed.
"""
from decimal import Decimal as D


def mass_difference_percent(base):
    """Difference between 13.7 g and 11.4 g relative to explicit base."""
    return (D('13.7') - D('11.4')) / D(str(base)) * D('100')


def angular_fraction():
    return D('360') * D('13.7') / D('100')


def unit_count_for_tons(grams_per_ton):
    """13.7 tons / 13.7 g; requires specifying which ton."""
    return D('13.7') * D(str(grams_per_ton)) / D('13.7')


def summarize():
    return {
        'metric_shock_pct_buyer_11_4_baseline': str(mass_difference_percent('11.4')),
        'metric_shock_pct_seller_13_7_baseline': str(mass_difference_percent('13.7')),
        'angle_exact_degrees': str(angular_fraction()),
        'angle_rounded_1_decimal': str(angular_fraction().quantize(D('0.1'))),
        'unit_count_if_metric_ton': str(unit_count_for_tons('1000000')),
        'unit_count_if_US_short_ton': str(unit_count_for_tons('907184.74')),
        'unit_count_if_UK_long_ton': str(unit_count_for_tons('1016046.9088')),
        'note': 'No result proves a historical standard, navigation practice, market value loss, correlation, or AI predictive accuracy.'
    }


if __name__ == '__main__':
    import json
    print(json.dumps(summarize(), indent=2))
