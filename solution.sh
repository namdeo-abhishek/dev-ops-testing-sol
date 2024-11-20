#!/bin/bash -xe

# Set the source and destination paths
SOURCE_ZIP="$HOME/$NAME/stub.zip"
DEST_ZIP="/tmp/archive.zip"
EXTRACT_DIR="/tmp/stub_extracted"
FINAL_DIR="/tmp/final_archive"

# Clean up previous runs
rm -rf "$EXTRACT_DIR" "$FINAL_DIR"
rm -f "$DEST_ZIP"

# Step 1: Check if the source zip file exists
if [ ! -f "$SOURCE_ZIP" ]; then
    echo "Source zip file ($SOURCE_ZIP) does not exist."
    exit 1
fi

# Step 2: Extract the contents of stub.zip
mkdir -p "$EXTRACT_DIR"
unzip -q "$SOURCE_ZIP" -d "$EXTRACT_DIR"

ls -lrth "$EXTRACT_DIR"

# Step 3: Filter out empty files (empty1, empty2) and rename non-empty files to have .txt extension
mkdir -p "$FINAL_DIR"
mylist=""
for file in "$EXTRACT_DIR/tmp"/*; do
    if [ -s "$file" ]; then
        base_name=$(basename "$file")
        cp "$file" "$FINAL_DIR/${base_name}.txt"
        mylist="$mylist $FINAL_DIR/${base_name}.txt"
    fi
done

# Step 4: Create a new archive.zip with only cool1.txt and cool2.txt
cd "$FINAL_DIR" || exit 1
zip -r -q "$DEST_ZIP" $mylist

# Step 5: Check if archive.zip was created successfully
if [ -f "$DEST_ZIP" ]; then
    echo "Archive created successfully at $DEST_ZIP"
    exit 0
else
    echo "Failed to create archive."
    exit 1
fi