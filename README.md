# JSON Manager Script

A simple yet powerful Python tool designed to batch-add data to or update existing data in JSON files within a directory. It's particularly useful for managing multi-language translation files or JSON configuration files with a similar structure.

## Features

- **Batch Processing:** Processes all `.json` files in a specified target directory.
- **Flexible Updates:** Adds or updates data under a user-defined prefix key path.
- **Two Distinct Modes:**
    - `add`: Only adds new keys, skipping existing ones. (Default)
    - `update`: Overwrites the values of existing keys with new data.
- **Language-Code Aware:** Matches input data from your source JSON file to the target files based on their filenames (e.g., `en.json`, `de.json`).
- **Error Handling:** Includes checks for invalid JSON formats and issues with file or directory paths.

## How to Use

### Prerequisites

This script does not require any special library installations. You only need to have Python 3 installed on your system.

### Usage

The script is executed from the command line and accepts several arguments.

```bash
python json_manager.py -i <input_file> -t <target_directory> -p <prefix_path> -a <action>

    Parameters:

    -i, --input-file (Required): The path to the JSON file containing the data to be added or updated. This file should contain data keyed by language codes (e.g., {"en": {...}, "de": {...}}).

    -t, --target-directory (Required): The path to the directory containing the JSON files you want to update.

    -p, --prefix-path (Required): The key path where the new data should be added or updated (e.g., update.releaseNotes). Use a dot (.) to separate keys.

    -a, --action (Optional): The action to perform. Can be add (default) or update.

Example
    Let's say you have a file named new_translations.json with new translations you want to add to your existing translation files located in the translations directory.

    Content of new_translations.json:

    JSON

    {
    "en": {
        "newKey1": "This is a new English key."
    },
    "de": {
        "newKey1": "Das ist ein neuer deutscher Schlüssel."
    }
    }
    Content of translations/en.json (existing file):

    JSON

    {
    "header": {
        "title": "Welcome"
    }
    }
    To add the new data under the releaseNotes.new_features path in add mode, use the following command:

    Bash

    python json_manager.py -i new_translations.json -t translations -p releaseNotes.new_features -a add
    After running the command, the translations/en.json file will be updated as follows:

    JSON

    {
    "header": {
        "title": "Welcome"
    },
    "releaseNotes": {
        "new_features": {
        "newKey1": "This is a new English key."
        }
    }
    }
    Note: If the releaseNotes key does not exist, the script will automatically create it.

Contributing
I welcome your feedback and contributions! If you find any bugs or have a feature suggestion, please feel free to open an Issue or submit a Pull Request.