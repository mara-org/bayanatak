import json
import subprocess
import sys
import unittest


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "bayanatak.cli", *args],
        check=False,
        capture_output=True,
        text=True,
    )


class CliTests(unittest.TestCase):
    def test_user_json_output_is_machine_readable(self):
        result = run_cli("user", "--count", "2", "--seed", "4", "--format", "json")

        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(len(data), 2)
        self.assertTrue(data[0]["is_fake"])

    def test_checkout_csv_has_expected_columns(self):
        result = run_cli("checkout", "--count", "1", "--seed", "2", "--format", "csv")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("order_id", result.stdout)
        self.assertIn("total_sar", result.stdout)

    def test_form_defaults_to_signup(self):
        result = run_cli("form", "--count", "1", "--format", "json")

        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data[0]["form_type"], "signup")

    def test_invalid_city_exits_with_argparse_error(self):
        result = run_cli("user", "--city", "unknown")

        self.assertEqual(result.returncode, 2)

    def test_default_command_outputs_users(self):
        result = run_cli()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("name_ar", result.stdout)


if __name__ == "__main__":
    unittest.main()
