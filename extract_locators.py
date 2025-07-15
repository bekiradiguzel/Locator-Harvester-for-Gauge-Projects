import os
import re


def extract_locators_from_cpt_file(file_path):
    """
    Extracts various locators from a given Gauge .cpt file.
    Looks for the new 'generic_locator' pattern.
    """
    # Initialize found_locators with the new 'generic_locator' key
    found_locators = {
        "generic_locator": set(),
        # If you still want to differentiate by type later, you'd add more logic
        # For now, all extracted quoted strings go into 'generic_locator'
    }

    # regex patterns
    patterns = {
        "generic_locator": re.compile(
            r'(?:on the|into the|to the|the)\s+"([^"]+)"\s*(?:element|link|field|button)?'
        ),

    }

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            # Iterate through the patterns
            for locator_type, pattern in patterns.items():
                matches = pattern.finditer(content)
                for match in matches:
                    locator_value = match.group(1)
                    found_locators[locator_type].add(locator_value)
    except Exception as e:
        print(f"DEBUG: Error processing {file_path}: {e}")
    return found_locators


def main():
    """
    Main function to scan the project directory and collect all locators from .cpt files.
    """
    project_root = input(
        "Enter the root path of your Java Selenium Gauge project (where .cpt files are): "
    )

    print(f"DEBUG: You entered: '{project_root}'")

    if not os.path.isdir(project_root):
        print(
            f"ERROR: The path '{project_root}' is not a valid directory or does not exist."
        )
        print("Please ensure the path is correct and accessible.")
        return

    # Initialize all_extracted_locators with the new 'generic_locator' key
    all_extracted_locators = {
        "generic_locator": set(),
    }
    cpt_files_processed = 0
    total_files_scanned = 0

    print(f"\n--- Starting locator extraction from: {project_root} ---")

    for root, dirs, files in os.walk(project_root):
        print(f"DEBUG: Scanning directory: '{root}'")

        for file in files:
            total_files_scanned += 1
            if file.endswith(".cpt"):
                cpt_files_processed += 1
                file_path = os.path.join(root, file)
                print(f"Processing CPT file: '{file_path}'")
                current_file_locators = extract_locators_from_cpt_file(
                    file_path
                )

                # Ensure you iterate over the key
                for (
                    locator_type
                ) in (
                    all_extracted_locators
                ):  # This will now be 'generic_locator'
                    all_extracted_locators[locator_type].update(
                        current_file_locators[locator_type]
                    )
            else:
                print(
                    f"DEBUG: Skipping non-CPT file: '{os.path.join(root, file)}'"
                )

    print("\n--- Extraction Complete ---")
    print(f"Total files scanned (all types): {total_files_scanned}")
    print(f"Processed {cpt_files_processed} CPT files.")

    output_dir = "extracted_locators_cpt"
    os.makedirs(output_dir, exist_ok=True)

    total_unique_locators = 0
    # Loop over the 'generic_locator' key
    for locator_type, locators_set in all_extracted_locators.items():
        file_name = os.path.join(output_dir, f"{locator_type}_locators.txt")
        num_locators = len(locators_set)
        total_unique_locators += num_locators

        if num_locators > 0:
            with open(file_name, "w", encoding="utf-8") as f:
                for locator in sorted(list(locators_set)):
                    f.write(locator + "\n")
            # Update print message
            print(
                f"Found {num_locators} unique {locator_type.replace('_', ' ').capitalize()} locators. Saved to '{file_name}'"
            )
        else:
            # Update print message
            print(
                f"No {locator_type.replace('_', ' ').capitalize()} locators found."
            )

    print(f"\nTotal unique locators extracted: {total_unique_locators}")
    print(f"All extracted locators are saved in the '{output_dir}' directory.")


if __name__ == "__main__":
    main()
