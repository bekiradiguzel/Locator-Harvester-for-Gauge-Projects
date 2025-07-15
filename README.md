# Locator-Harvester-for-Gauge-Projects
This Python script helps QA automation engineers extract web element locators from Gauge .cpt (concept) files. It scans your project, finds locators defined within your test steps, and saves them to organized text files.
Web Element Locator Harvester for Gauge Projects
This Python script helps QA automation engineers extract web element locators from Gauge .cpt (concept) files. It scans your project, finds locators defined within your test steps, and saves them to organized text files.

✨ Features
Scans Project Directories: Recursively searches for .cpt files.

Extracts Quoted Locators: Identifies strings enclosed in double quotes within your English Gauge steps (e.g., "//input[@id='username']").

Handles Duplicates: Uses sets to ensure only unique locators are collected.

Organized Output: Saves extracted locators into a dedicated extracted_locators_cpt directory.

🚀 How to Use
Prerequisites
Python 3.x (tested with Python 3.9+)

Save the Files:

Save the main script as extract_locators.py.

Save the unit test script as test_locator_extractor.py.

Place both files in your project's root or a convenient location.

Run the Main Script:
Open your terminal or command prompt, navigate to the directory where you saved extract_locators.py, and run:

python extract_locators.py



The script will ask you to enter the root path of your Gauge project. Upon successful execution, a new directory named extracted_locators_cpt will be created in the script's location, containing .txt files categorized by the extracted locator values.

Run the Unit Tests (Optional but Recommended):
To verify the script's functionality, run the unit tests from your terminal:

python test_locator_extractor.py



This will execute tests that validate the locator extraction logic.

📚 Example Gauge Step Format
This script is specifically designed to extract the quoted locator strings from Gauge steps formatted as follows in your .cpt files:

* Wait for and click on the "//span[normalize-space()='Account & Lists']" element.
* Enter "email@email.com" into the "//input[@id='ap_email_login']" element.
* Wait for and click on the "//input[@type='submit']" element.


🔍 How Locators Are Identified
The script uses Regular Expressions (Regex) to find and extract the locator strings. It looks for a specific pattern within each line of your .cpt files.

The core regex pattern used is:
r'(?:on the|into the|to the|the)\s+"([^"]+)"\s*(?:element|link|field|button)?'

Let's break down this pattern:

(?:on the|into the|to the|the): This part matches common phrases that precede a locator, such as "on the", "into the", "to the", or simply "the". The ?: makes it a non-capturing group.

\s+: Matches one or more whitespace characters.

": Matches the opening double quote before your locator string.

([^"]+): This is the key part that captures your locator string.

[^"]: Matches any character that is not a double quote.

+: Means "one or more times."

The parentheses () around [^"]+ create a capturing group, meaning whatever matches this part will be extracted as the locator value.

": Matches the closing double quote after your locator string.

\s*: Matches zero or more whitespace characters.

(?:element|link|field|button)?: This optional part matches common words that might follow the locator, like "element", "link", "field", or "button". The ? makes this entire group optional.

When the script finds a match, it extracts the content from the capturing group (([^"]+)), which is your actual XPath, CSS selector, ID, or partial text.

💡 Why This Tool is Useful
Locator Auditing: Quickly get an inventory of all locators used across your test suite.

Refactoring Aid: Identify locators that might be duplicated or need updating during UI changes.

Documentation: Provides a clear list of elements interacted with by your automation.

Showcases Practical QA Automation Skills: This project effectively demonstrates your proficiency in Python, including file system navigation, robust regular expression usage for parsing, efficient data handling with sets, and a commitment to code quality through unit testing – all directly applicable to modern QA automation roles.

✅ Unit Tests
The project includes a test_locator_extractor.py file with unit tests to ensure the locator extraction logic works as expected. These tests cover various scenarios, including basic extraction, duplicate handling, and files with no matching patterns.
