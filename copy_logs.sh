#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <new_folder_name>"
    exit 1
fi

# Extract arguments
NEW_FOLDER=$1
SOURCE_FOLDER=/media/polyblank/MicroPython/logs
#echo $SOURCE_FOLDER

# Check if the source folder exists
if [ ! -d "$SOURCE_FOLDER" ]; then
    echo "Error: Source folder '$SOURCE_FOLDER' does not exist."
    exit 1
fi

# Check if the target folder exists
if [ -d "$NEW_FOLDER" ]; then
    echo "Folder '$NEW_FOLDER' already exists. Copying files..."
else
    mkdir -p "$NEW_FOLDER"
    echo "Created folder: $NEW_FOLDER"
fi

# Copy files from the source folder to the new folder
mv "$SOURCE_FOLDER"/* "$NEW_FOLDER"/
echo "Copied files from $SOURCE_FOLDER to $NEW_FOLDER"
