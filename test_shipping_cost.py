import unittest
from random import randrange

from parameterized import parameterized

from calculate_shipping import (calculate_shipping_cost,
                                MINIMAL_PRICE, ShippingUnavailableError)


class TestShippingCost(unittest.TestCase):

    @parameterized.expand([
        [2, 'large', True, "extremely high", 880],
        [5, 'large', True, "extremely high", 960],
        [10, 'large', False, "extremely high", 480],
        [15, 'large', False, "extremely high", 640],
        [30, 'large', False, "extremely high", 640],
        [31, 'large', False, "extremely high", 800],
    ])
    def test_distance(self, distance, dimensions,
                      is_fragile, service_workload, expected):

        self.assertEqual(calculate_shipping_cost(
            distance, dimensions, is_fragile, service_workload), expected)

    @parameterized.expand([
        [randrange(31, 100), 'small', False, 'high', 560],
        [randrange(31, 100), 'large', False, 'high', 700],
    ])
    def test_dimensions(self, distance, dimensions,
                        is_fragile, service_workload, expected):
        self.assertEqual(calculate_shipping_cost(
            distance, dimensions, is_fragile, service_workload), expected)

    @parameterized.expand([
        [randrange(11, 31), 'large', True, 'normal', 700],
        [randrange(11, 31), 'large', True, 'increased', 840],
        [randrange(11, 31), 'large', True, 'high', 980],
        [randrange(11, 31), 'large', True, 'extremely high', 1120],
    ])
    def test_workload(self, distance, dimensions,
                      is_fragile, service_workload, expected):
        self.assertEqual(calculate_shipping_cost(
            distance, dimensions, is_fragile, service_workload), expected)

    @parameterized.expand([
        [1, 'small', False, 'normal', MINIMAL_PRICE],
    ])
    def test_minimal_price(self, distance, dimensions,
                           is_fragile, service_workload, expected):
        self.assertEqual(calculate_shipping_cost(
            distance, dimensions, is_fragile, service_workload), MINIMAL_PRICE)

    def test_calculate_fragile(self):
        with self.assertRaises(ShippingUnavailableError):
            calculate_shipping_cost(distance=31, dimensions='small',
                                    is_fragile=True, service_workload='normal')

    @parameterized.expand([
        [randrange(11, 31), 'large', True, 'high', 980],
        [randrange(11, 31), 'large', False, 'high', 560],
    ])
    def test_calculate_fragile(self, distance, dimensions,
                               is_fragile, service_workload, expected):
        self.assertEqual(calculate_shipping_cost(
            distance, dimensions, is_fragile, service_workload), expected)
