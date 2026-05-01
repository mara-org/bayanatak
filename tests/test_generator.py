import re
import unittest

from bayanatak.generator import GenerateOptions, city_slugs, generate_checkouts, generate_forms, generate_users


class GeneratorTests(unittest.TestCase):
    def test_users_are_deterministic_with_seed(self):
        options = GenerateOptions(count=3, seed=42)

        self.assertEqual(generate_users(options), generate_users(options))

    def test_safe_phone_mode_is_not_dialable_digits(self):
        users = generate_users(GenerateOptions(count=2, seed=1))

        self.assertTrue(all("X" in user["phone"] for user in users))
        self.assertTrue(all(not user["phone"].isdigit() for user in users))

    def test_digits_phone_mode_matches_saudi_shape(self):
        users = generate_users(GenerateOptions(count=3, seed=1, phone_mode="digits"))

        self.assertTrue(all(re.fullmatch(r"05\d{8}", user["phone"]) for user in users))

    def test_city_filter_uses_requested_city(self):
        users = generate_users(GenerateOptions(count=5, seed=3, city="riyadh"))

        self.assertEqual({user["city"] for user in users}, {"الرياض"})

    def test_checkouts_include_local_commerce_fields(self):
        orders = generate_checkouts(GenerateOptions(count=2, seed=5, city="jeddah"))

        self.assertEqual(len(orders), 2)
        self.assertTrue(all(order["city"] == "جدة" for order in orders))
        self.assertTrue(all(order["total_sar"] > 0 for order in orders))
        self.assertTrue(all(order["is_fake"] is True for order in orders))

    def test_signup_forms_are_flat_for_ui_testing(self):
        forms = generate_forms("signup", GenerateOptions(count=2, seed=8))

        self.assertEqual({form["form_type"] for form in forms}, {"signup"})
        self.assertTrue(all("full_name" in form for form in forms))
        self.assertTrue(all(form["is_fake"] for form in forms))

    def test_unknown_form_type_raises(self):
        with self.assertRaises(ValueError):
            generate_forms("unknown", GenerateOptions())

    def test_city_slugs_are_stable(self):
        self.assertIn("riyadh", city_slugs())
        self.assertEqual(city_slugs(), sorted(city_slugs()))


if __name__ == "__main__":
    unittest.main()
