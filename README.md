# VOC File Organiser 🧬🗂️

A GUI application designed to organize and restructure raw Volatile Organic Compound (VOC) sensor data files from the analyzer. This tool helps researchers and technicians efficiently manage their sensor data by automatically organizing files into structured folders based on test repeats.

## Features

- **File Organization**: Automatically organizes sensor data files into separate folders based on test repeats
- **Custom Naming**: Flexible file naming system with support for:
  - Test numbers (`<number>`)
  - Dates (`<date>`)
  - Timestamps (`<time>`)
- **Batch Processing**: Process multiple files at once
- **Compression**: Option to compress output as ZIP files
- **User-Friendly Interface**: Simple GUI with clear instructions and help system

## Requirements

- Python 3.x
- PyQt6
- See `requirements.txt` for full dependency list

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Launch the application
2. Select the source folder containing your raw sensor data files
3. Choose a destination folder for the organized files
4. (Optional) Configure file naming settings:
   - Enter desired name format using available placeholders
   - Choose whether to apply naming to file names and/or experiment names
5. (Optional) Enable compression if desired
6. Click "Convert files" to process the data

### Name Format Placeholders

- `<number>`: Test number
- `<date>`: Date from the sensor file
- `<time>`: Time from the sensor file

Example format: `Day <number> <date> <time>`

## Input File Requirements

The sensor data files should be text files (.txt) containing the following fields:
- Experiment name
- Repeat number (in format X/Y)
- Time (HH:MM:SS)
- Date (DD/MM/YYYY)

## Building Executable

To build a standalone executable:

1. Ensure PyInstaller is installed
2. Run the build script:
   ```bash
   ./buildexe.sh
   ```

## Version

Current version: 1.1

## Author

Created by Alex Dowsett, University of Surrey
