 # File Processing Tool Readme

## Overview

This repository contains two Python scripts designed for processing files in a directory and handling GUI operations through a Tkinter-based application. The primary functionalities include identifying file types within a selected directory and listing PDF files.

## Scripts

### `gui.py`

#### Functions:
1. **start_processing()**
   - This function initiates processing on the selected directory. It updates status messages based on whether the operation is successful or encounters an error.
   
2. **process_directory(input_path)**
   - This function should be implemented to handle specific operations with files in `input_path`. The exact implementation details are not provided in this document but would involve using functions from `file_utils.py`.

#### Usage:
To run the GUI application, ensure you have Tkinter installed and then execute `gui.py` script. It will open a window to select a directory for processing.

```bash
python gui.py
```

## Directory Structure

The repository contains two scripts (`file_utils.py` and `gui.py`) in the root directory. There are no subdirectories or additional files included in this structure, unless they are commonly used configuration files like `.gitignore`.

## Dependencies

- Python 3.x
- Tkinter (standard library for Python)

Ensure you have these installed to run the application and scripts correctly.

## Contribution

If you wish to contribute, please fork this repository and submit a pull request with your changes or enhancements. For major changes, consider opening an issue first to discuss what you would like to change.

## License

This project is open-source and available under the MIT License. Please refer to the `LICENSE` file for more details.

---

Thank you for using this tool! If you have any questions or need further assistance, feel free to reach out.
