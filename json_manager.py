import json
import os
import argparse

description_text = """A tool to add or update data in all JSON files within a specified directory.

--------------------------------------------------------------------------------
INPUT FILE FORMAT:
--------------------------------------------------------------------------------
The input file should be a JSON object with language names as top-level keys.

Example Format:
{
  "en": {
    "newFeatureTitle": "Exciting New Feature",
    "welcomeMessage": "Welcome to our app! We have a new feature for you.",
    "buttonLabel": "Check it out"
  }
}
Please ensure the language names in this file match your target files (e.g., 'en' for 'en.json').
"""

def main():
    """
    Main function to update all JSON files in a directory based on user input.
    """
    parser = argparse.ArgumentParser(
        description=description_text,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--input-file',
        '-i',
        required=True,
        help='Path to the input file. See the above description for format details.'
    )
    parser.add_argument(
        '--target-directory',
        '-t',
        required=True,
        help='Path to the directory containing the JSON files to be updated.'
    )
    parser.add_argument(
        '--prefix-path',
        '-p',
        required=True,
        help='The prefix key path to be prepended to each new key (e.g., update.releaseNotes).'
    )
    parser.add_argument(
        '--action',
        '-a',
        choices=['add', 'update'],
        default='add',
        help='The action to perform: "add" (add new keys) or "update" (overwrite existing keys). Default: add.'
    )
    args = parser.parse_args()

    # Check if input and target paths exist
    if not os.path.exists(args.input_file):
        print(f"Error: Input file not found: {args.input_file}")
        return
    
    if not os.path.isdir(args.target_directory):
        print(f"Error: Target directory not found or is not a directory: {args.target_directory}")
        return

    try:
        # Read data from the input file
        with open(args.input_file, 'r', encoding='utf-8') as f:
            all_new_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Input file has an invalid JSON format: {args.input_file}")
        return
    except Exception as e:
        print(f"Error: An issue occurred while reading the input file: {e}")
        return
    
    print(f"\nUpdating all JSON files in the '{args.target_directory}' directory... (Action: {args.action})\n")
    
    # Loop through each file in the target directory
    for filename in os.listdir(args.target_directory):
        # Process only .json files
        if filename.endswith('.json'):
            current_lang_code = filename.replace('.json', '')

            # Find matching data in the input JSON
            if current_lang_code in all_new_data:
                current_file_path = os.path.join(args.target_directory, filename)
                
                print(f"-> Processing '{current_lang_code}' language file: {current_file_path}")

                try:
                    with open(current_file_path, 'r', encoding='utf-8') as f:
                        target_data = json.load(f)

                    # Check if the prefix path exists and is a dictionary
                    keys = args.prefix_path.split('.')
                    current_level = target_data
                    path_found = True
                    for key in keys:
                        if key not in current_level:
                            if args.action == 'add':
                                current_level[key] = {}
                            else:
                                path_found = False
                                break
                        elif not isinstance(current_level[key], dict):
                            # If a part of the path is not a dictionary, raise an error
                            print(f"Error: '{key}' key is not a dictionary. The path '{args.prefix_path}' cannot be used.")
                            path_found = False
                            break
                        current_level = current_level[key]
                    
                    if not path_found:
                        print(f"Warning: The path '{args.prefix_path}' does not exist or is invalid. Skipping file.")
                        continue

                    # Process the new data for the current language
                    new_keys_for_this_lang = all_new_data[current_lang_code]
                    for key_to_add, value in new_keys_for_this_lang.items():
                        if key_to_add in current_level and args.action == 'add':
                            print(f"Warning: '{args.prefix_path}.{key_to_add}' key already exists, 'add' operation is being skipped.")
                        else:
                            current_level[key_to_add] = value
                            print(f"'{args.prefix_path}.{key_to_add}' key {'added' if args.action == 'add' else 'updated'}.")
                    
                    # Write the updated JSON back to the file
                    with open(current_file_path, 'w', encoding='utf-8') as f:
                        json.dump(target_data, f, indent=4, ensure_ascii=False)
                    
                    print(f"File successfully updated: {current_file_path}\n")

                except json.JSONDecodeError:
                    print(f"Error: '{current_file_path}' has an invalid JSON format.")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")

            else:
                print(f"Warning: No input data found for '{current_lang_code}', skipping file.")
    
    print("\nAll operations completed.")

if __name__ == "__main__":
    main()