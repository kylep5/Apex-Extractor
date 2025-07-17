'''
Start date: June 7th, 2025
Description: This script extracts data from the ApexWear app and saves it as a CSV file.
Requires the ADB tool to be installed, the device to be connected, and Git for Windows to be installed.
Part of the Apex Extractor project (https://github.com/kylep5/Apex-Extractor)
'''

# Imports ------------------------
import sqlite3
import json
import os


# Functions ---------------------
def pull_latest_database():
    import subprocess

    print("Attempting to pull lastest database from device...")

    is_successful = False

    package_name = "com.dongxin.watch_app"
    db_on_phone = "sport.db"
    final_db_name = "sport.db"
    temp_tar_name = "sport_backup.tar"

    try:
        # Remove any existing temp database file
        if os.path.exists(temp_tar_name):
            os.remove(temp_tar_name)

        # Pull binary data to a .tar file
        adb_command = ["adb", "exec-out", f"run-as {package_name} tar c databases/{db_on_phone}"]

        # Run adb command
        adb_process_result = subprocess.run(adb_command, check=True, capture_output=True)

        database_bytes = adb_process_result.stdout

        if not database_bytes:
            print("Error: ADB command ran but returned no data")
            return False
        
        with open(temp_tar_name, "wb") as f:
            f.write(database_bytes)
        
        print(f"Successfully created temp tar file: {temp_tar_name}")

        # Create tar extraction command
        tar_command = ["tar", "-xf", temp_tar_name, "--strip-components=1"]

        # If command was successful, check if temp file is valid
        if not os.path.exists(temp_tar_name) or os.path.getsize(temp_tar_name) == 0:
            print("Error: The pulled database file is empty or does not exist. If your device is disconnected, this is expected.")
            return False
        
        print("Successfully created temp archive: {temp_tar_name}")

        # Run tar command to extract the database
        subprocess.run(tar_command, check=True)

        if os.path.exists(final_db_name):
            print(f"'{final_db_name} is now up to date.")
            is_successful = True
        
        else:
            # If ADB connects but sends no data
            print("Error: Extraction failed, final database file not found.")
            is_successful = False
        
        
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"An error occurred while pulling the database: {e}.\nUsing existing local database file if available.")
        is_successful = False

    finally:
        # Clean up temp file if it exists
        if os.path.exists(temp_tar_name):
            os.remove(temp_tar_name)
            print(f"Removed temporary file: {temp_tar_name}")
    
    return is_successful
        
    
def export_to_csv(cursor, table_name, json_column, value_key, output_file, value_header):
    try:
        cursor.execute(f"SELECT {json_column} FROM {table_name}")
        rows = cursor.fetchall()
        print(f"Found {len(rows)} records in the table {table_name}.")

        with open(output_file, "w", newline="") as csvfile:
            csvfile.write(f"Timestamp_ms, {value_header}\n")
            total_measurements = 0

            # Loop through each row and extract the data
            for row in rows:
                json_string = row[0]

                try:
                    data_points = json.loads(json_string)
                    for entry in data_points:
                        timestamp = entry.get("currentTime")
                        value = entry.get(value_key)

                        # Write into CSV file if both timestamp and value are present
                        if timestamp is not None and value is not None:
                            csvfile.write(f"{timestamp},{value}\n")
                            total_measurements += 1
                
                except (json.JSONDecodeError, TypeError):
                    print(f"Error: Could not parse a JSON string in table {table_name}.")
        
        print(f"Total measurements written to {output_file}: {total_measurements}")

    except sqlite3.Error as e:
        # For errors related to "no such table"
        print(f"Database error while processing table {table_name}: {e}")



# Main ------------------------------

def main():

    # Main function extracts all important data from the database and saves it to a CSV file.

    DB_FILE = "sport.db"
    conn = None

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        print("Connected to the database successfully.")


        # Exports all data to separate CSV files


        # Heart Rate Data
        export_to_csv(cursor, 
                      table_name="HEART_DATA_CACHE",
                      json_column="DATA_LIST",
                      value_key="hr_value",
                      output_file="heart_rate_data.csv",
                      value_header="HeartRate"
                      )
        

        # Sleep Data
        export_to_csv(cursor, 
                      table_name="SLEEP_DATA_CACHE",
                      json_column="DATA_LIST",
                      value_key="sleepType",
                      output_file="sleep_data.csv",
                      value_header="SleepValue"
                      )
        
        # Blood Oxygen Data
        export_to_csv(cursor, 
                      table_name="BLOOD_OXYGEN_CACHE",
                      json_column="BLOOD_DATA_LIST",
                      value_key="blood_oxygen_value",
                      output_file="blood_oxygen_data.csv",
                      value_header="BloodOxygenValue"
                      )
        
        # Stress Data
        export_to_csv(cursor, 
                      table_name="PRESS_DATA_CACHE",
                      json_column="DATA_LIST",
                      value_key="press_value",
                      output_file="stress_data.csv",
                      value_header="StressLevel"
                      )
        

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()
            print("Database connection closed.")



if __name__ == "__main__":


    # Try to pull the latest database from the device
    if pull_latest_database():
        # If successful
        print("Database pull successful. Processing fresh data...")
        main()
    else:
        # If failed
        print("\nCould not pull the latest database.")

        if os.path.exists("sport.db"):
            # Using the existing database file
            print("Using existing database file 'sport.db'.")
            print("Processing existing data...")
            main()
        
        else:
            # If no database file exists
            print("No device connected and no local database file found.\nPlease connect your phone or place a 'sport.db' file in the folder.")


