import os
import sqlite3
import shutil

# Define paths to the backup and output directories
backup_directory = f"{os.path.expanduser('~')}/libimobiledevice/bu/00008030-0008186A1E20802E"
output_directory = f"{os.path.expanduser('~')}/datsets"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Connect to the Manifest database
try:
    conn = sqlite3.connect(os.path.join(backup_directory, 'Manifest.db'))
    cursor = conn.cursor()
except sqlite3.Error as e:
    print(f"Failed to connect to the database: {e}")
    exit(1)


# Function to query files from the database
def query_files(cursor):
    cursor.execute("SELECT fileID, domain, relativePath FROM Files")
    yield from cursor.fetchall()


# Function to copy a file
def copy_file(source_file_path, destination_file_path):
    if not os.path.exists(source_file_path):
        return False
    os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)
    shutil.copyfile(source_file_path, destination_file_path)
    return True


# Function to extract files from the backup
def extract_files(cursor, output_directory):
    for file_id, domain, relative_path in query_files(cursor):
        source_file_path = os.path.join(backup_directory, file_id[:2], file_id)
        output_directory_path = os.path.join(output_directory, domain, relative_path)
        if copy_file(source_file_path, output_directory_path):
            print(f"Copied file from {source_file_path} to {output_directory_path}")
        else:
            print(f"File not found: {source_file_path}")


extract_files(cursor, output_directory)
conn.close()
