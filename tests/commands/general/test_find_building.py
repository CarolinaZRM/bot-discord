import logging
import unittest

from controllers.find_building import get_building_information


class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        logging.error("hasca")
        self.assertEqual("foo".upper(), "FOO")

    def test_all_letter_dash(self):
        salon = "f-a"
        info_ = get_building_information(salon)
        logging.debug(info_)
        self.assertEqual(info_.get("name"), "Física")
        self.assertEqual(
            info_.get("gmaps_loc"), "https://goo.gl/maps/mTX7tjLDQK8zzc5W6"
        )

    def test_all_letter_without_dash(self):
        salon = "fa"
        info_ = get_building_information(salon)
        self.assertIsNone(info_)

    def test_one_letter_digits(self):
        salon = "s123"
        info_ = get_building_information(salon)
        self.assertIsNotNone(info_)
        self.assertEqual(info_.get("name"), "Luis Stefani (Ingeniería)")

    def test_one_letter_digits_dash(self):
        salon = "M-123"
        info_ = get_building_information(salon)
        self.assertIsNotNone(info_)
        self.assertEqual(info_.get("name"), "Luis Monzón (Matemáticas)")

    def test_two_letter_digits(self):
        salon = "ch123"
        info_ = get_building_information(salon)
        self.assertIsNotNone(info_)
        self.assertEqual(info_.get("name"), "Chardón")

    def test_two_letter_digits_dash(self):
        salon = "ae-123"
        info_ = get_building_information(salon)
        self.assertIsNotNone(info_)
        self.assertEqual(info_.get("name"), "Administración de Empresas")


if __name__ == "__main__":
    unittest.main(verbosity=1)
