# Apex Extractor

## Personal Fitness Data Exporter for ApexWear Android App

**Apex Extractor** is a Python script designed to help users extract their personal fitness and health data from the **ApexWear mobile application** by directly accessing its local database on compatible Android devices. It automates the process of pulling the `sport.db` file from the device via ADB and transforming key health metrics into easily consumable CSV files for custom analysis and visualization.

This project showcases data extraction, parsing, and automation skills, providing a valuable tool for anyone looking to gain deeper insights into their health data beyond the confines of the official application by allowing them to potentially import their historical fitness metrics into other compatible applications or platforms that support CSV data imports.

## Features

- **Automated Database Pull:** Uses ADB to directly pull the `sport.db` SQLite database from the device's internal application data directory (`/data/data/com.dongxin.watch_app/databases/sport.db`).
    
- **Comprehensive Data Extraction:** Extracts detailed information into separate CSV files, including:
    
    - **Heart Rate Data:** Historical `hr_value` measurements from `HEART_DATA_CACHE`.
        
    - **Sleep Data:** `sleepType` records from `SLEEP_DATA_CACHE`.
        
    - **Blood Oxygen Data:** `blood_oxygen_value` readings from `BLOOD_OXYGEN_CACHE`.
        
    - **Stress Data (Blood Pressure):** `press_value` levels from `PRESS_DATA_CACHE`.
        
    - All CSVs include UNIX timestamps (`currentTime`).
        
- **CSV Export:** Converts raw database entries, typically stored as JSON strings within database fields, into individual, human-readable CSV files.
    
- **Error Handling:** Includes checks for ADB connectivity, database file validity, and JSON parsing errors to provide informative feedback.
    

## Technologies Used

- **Python 3.12+**
    
- **`sqlite3`:** For interacting with the SQLite database.
    
- **`json`:** For parsing JSON strings embedded within database fields.
    
- **`os`:** For file system operations (e.g., managing temporary files).
    
- **`subprocess`:** For executing ADB and `tar` commands.
    
- **ADB (Android Debug Bridge):** The primary tool for communicating with the Android device.
    
- **`tar` (command-line utility):** Used on the device side via ADB (`adb exec-out run-as`) to package the database file for transfer.
    

## Prerequisites

Before running the script, ensure you have the following set up:

- **Python 3.12 or newer** installed on your computer.
    
- **Git** installed (for cloning this repository).
    
- **ADB (Android Debug Bridge)** installed and configured on your computer, and accessible from your system's PATH.
    
- **An Android device:**
    
    - With **ADB debugging enabled** in Developer Options.
        
    - Connected to your computer via USB.
        
    - The **ApexWear mobile application** (`com.dongxin.watch_app`) must be installed and running on your device, ensuring the `sport.db` file is present.
        
    - **Access to the application's internal data directory** (specifically `/data/data/com.dongxin.watch_app/databases/sport.db`) via ADB's `run-as` command. (On some devices or app versions, additional configurations or permissions may be required to enable ADB to pull app-private data.)
        

## Installation

1. **Clone the repository:**
    
    Bash
    
	i.
    ```
    git clone https://github.com/kylep5/Apex-Extractor.git
	```
	
	ii.
	```
    cd Apex-Extractor
    ```
    
2. **No additional Python dependencies** are required beyond standard library modules.
    

## Usage

1. **Ensure your Android device is connected** via USB and ADB debugging is enabled.
    
2. **Run the script** from your terminal in the `Apex-Extractor` directory:
    
    Bash
    
    ```
    python apexExtractor.py
    ```
    
3. The script will attempt to pull the `sport.db` file from your device.
    
    - If successful, it will process the database and generate the following CSV files in the same directory: `heart_rate_data.csv`, `sleep_data.csv`, `blood_oxygen_data.csv`, and `stress_data.csv`.
        
    - If the database pull fails, the script will attempt to use an existing `sport.db` file if found in the current directory.
        
    - If no device is connected and no local file is found, it will guide the user accordingly.
        

### Troubleshooting ADB Access

If the script encounters a "Permission Denied" or "Error pulling database" message during the ADB database pull, consider the following common reasons:

- **ADB Authorization:** You might need to accept the "Allow USB debugging?" prompt on your Android device when first connecting it to your computer.
    
- **Device Connectivity:** Verify your device is recognized by ADB by running `adb devices`.
    
- **App Data Access Restrictions:** Modern Android versions impose stricter limitations on accessing app-private data (`/data/data/`). The `adb run-as` command is used, but its functionality can depend on the application's manifest settings and the device's security policies. Ensure your device and the application's current state permit this level of ADB access.
## How It Works (Technical Overview)

The script automates the data extraction process by first attempting to acquire the `sport.db` file from the connected Android device. This is achieved by utilizing ADB's `exec-out` command in conjunction with the `run-as` utility, which allows the script to execute commands as the target application (`com.dongxin.watch_app`). It then uses the standard `tar` command (executed on the device's side) to create a compressed archive of the database file, streaming the binary data directly back to the local Python script. The script then extracts this `sport.db` file locally.

Once the `sport.db` file is obtained, the Python script connects to it using the `sqlite3` module. It proceeds to query specific tables (`HEART_DATA_CACHE`, `SLEEP_DATA_CACHE`, `BLOOD_OXYGEN_CACHE`, `PRESS_DATA_CACHE`) where detailed health data is stored. Since much of this data is embedded within JSON strings in database columns, the script uses the `json` module to parse these strings. For each relevant record, it extracts the `currentTime` (a UNIX timestamp in milliseconds) and its corresponding health `value` (e.g., `hr_value`, `sleepType`, `blood_oxygen_value`, `press_value`). Finally, this structured data is written into individual CSV files, making it readily available for external analysis, visualization, or integration with other tools.

## Contributing

This project is a personal initiative to demonstrate practical data engineering and automation skills. While direct contributions aren't expected for this specific personal project, feel free to fork the repository, adapt it to your specific needs, or explore its methodology.

## Disclaimer

This script is provided for educational purposes and personal data analysis only. The author makes no warranties or guarantees regarding its functionality, compatibility with future app versions, or legal permissibility in all contexts. Users are solely responsible for ensuring their use of this script and their methods of data acquisition comply with all applicable laws and the device manufacturer's terms of service.
