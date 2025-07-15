import unittest
import os
import sys
from extract_locators import extract_locators_from_cpt_file


class TestLocatorExtractor(unittest.TestCase):

    # Set up a temporary directory and dummy .cpt files for testing
    def setUp(self):
        self.test_dir = "test_data"
        os.makedirs(self.test_dir, exist_ok=True)

        self.cpt_file_basic = os.path.join(self.test_dir, "basic_test.cpt")
        with open(self.cpt_file_basic, "w") as f:
            f.write(
                """
* Wait for and click on the "//span[normalize-space()='Account & Lists']" element.
* Enter "email@email.com" into the "//input[@id='ap_email_login']" element.
* Wait for and click on the "//input[@type='submit']" element.
"""
            )

        self.cpt_file_duplicates = os.path.join(
            self.test_dir, "duplicates_test.cpt"
        )
        with open(self.cpt_file_duplicates, "w") as f:
            f.write(
                """
* Wait for and click on the "duplicate_xpath_value" element.
* Enter "some_text" into the "another_locator_value" element.
* Wait for and click on the "duplicate_xpath_value" element.
* Verify that the "yet_another_locator" element is visible.
"""
            )

        self.cpt_file_empty = os.path.join(self.test_dir, "empty_test.cpt")
        with open(self.cpt_file_empty, "w") as f:
            f.write("This file has no locators.\nJust some random text.")

        self.cpt_file_no_match = os.path.join(
            self.test_dir, "no_match_test.cpt"
        )
        with open(self.cpt_file_no_match, "w") as f:
            f.write(
                """
* This line has "a quoted string" but not in the target format.
* Another line without a specific locator pattern.
"""
            )

    # Clean up the temporary directory and files after all tests run
    def tearDown(self):
        for f in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, f))
        os.rmdir(self.test_dir)

    def test_basic_locator_extraction(self):
        locators = extract_locators_from_cpt_file(self.cpt_file_basic)
        # Assert against the 'generic_locator' key
        self.assertIn(
            "//span[normalize-space()='Account & Lists']",
            locators["generic_locator"],
        )
        self.assertIn(
            "//input[@id='ap_email_login']", locators["generic_locator"]
        )
        self.assertIn("//input[@type='submit']", locators["generic_locator"])
        # Adjust the expected count as well, as they are all under one key
        self.assertEqual(len(locators["generic_locator"]), 3)

        def test_duplicate_locator_handling(self):
            """Test that duplicate locators are stored only once (due to using sets)."""

        locators = extract_locators_from_cpt_file(self.cpt_file_duplicates)
        self.assertIn("duplicate_xpath_value", locators["generic_locator"])
        # Add assertions for other unique locators in the duplicates file if desired
        self.assertIn("another_locator_value", locators["generic_locator"])
        self.assertIn("yet_another_locator", locators["generic_locator"])
        self.assertEqual(len(locators["generic_locator"]), 3)

    def test_empty_cpt_file(self):
        locators = extract_locators_from_cpt_file(self.cpt_file_empty)
        self.assertTrue(
            not locators["generic_locator"]
        )  # Check if set is empty

    def test_no_matching_locators(self):
        locators = extract_locators_from_cpt_file(self.cpt_file_no_match)
        self.assertTrue(not locators["generic_locator"])

    def test_non_existent_file(self):
        non_existent_file = os.path.join(self.test_dir, "non_existent.cpt")
        locators = extract_locators_from_cpt_file(non_existent_file)
        self.assertTrue(not locators["generic_locator"])


if __name__ == "__main__":
    # Store the default stdout
    original_stdout = sys.stdout

    # Temporarily redirect sys.stdout to suppress the default unittest output entirely
    # This ensures ONLY your custom prints and the function's debug prints appear.
    # We still want to see the debug print, so we can't redirect to os.devnull here.
    # Instead, we'll let unittest print to a buffer and only show what we want.

    # We create a buffer to capture unittest's output
    import io

    buffer = io.StringIO()

    # Create a TextTestRunner instance, directing its output to our buffer
    runner = unittest.TextTestRunner(stream=buffer, verbosity=1)

    # Load tests from your test case class
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        TestLocatorExtractor
    )

    # Run the tests and capture the result.
    result = runner.run(suite)

    # After tests run, get the content from the buffer
    test_output = buffer.getvalue()

    # Restore stdout before printing anything
    sys.stdout = original_stdout

    # Now, print what you want to the actual console
    # You can choose to print the captured unittest output or just your custom message.

    # Option 1: Print the full unittest output (dots, summary, OK/FAIL) and then your message
    print(test_output)

    # Option 2: ONLY print the custom message and any debug lines from your function
    # To do this, you would need to parse `test_output` for the debug line
    # or ensure your function's debug print always goes to original_stdout.
    # For now, Option 1 is simpler and guarantees the standard test run info.

    if result.wasSuccessful():
        print("\n🎉 All tests passed successfully! 🎉")
    else:
        print(
            "\n❌ Some tests failed or encountered errors. Please check the output above. ❌"
        )
        # You might want to print the detailed errors if tests failed:
        # if result.errors:
        #     print("Errors:")
        #     for test, traceback_str in result.errors:
        #         print(f"  {test}:\n{traceback_str}")
        # if result.failures:
        #     print("Failures:")
        #     for test, traceback_str in result.failures:
        #         print(f"  {test}:\n{traceback_str}")
