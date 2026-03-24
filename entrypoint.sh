#!/bin/bash

# Verify that the correct number of arguments have been passed
if [ "$#" -lt 4 ] || [ "$#" -gt 5 ]; then
    echo "Usage: $0 <source_language> <target_language> <input_file> <output_file> [workflow]"
    exit 1
fi

# Assign arguments to variables
SOURCE_LANGUAGE=$1
TARGET_LANGUAGE=$2
INPUT_FILE=$3
OUTPUT_FILE=$4
WORKFLOW=$5

# Ensure the input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Input file $INPUT_FILE does not exist."
    exit 1
fi

# Build the command
CMD="python aphra_runner.py config.toml $SOURCE_LANGUAGE $TARGET_LANGUAGE $INPUT_FILE $OUTPUT_FILE"
if [ -n "$WORKFLOW" ]; then
    CMD="$CMD $WORKFLOW"
fi

# Execute the translation
$CMD

# Output a message with the output file name
OUTPUT_FILENAME=$(basename "$OUTPUT_FILE")
echo "Translation completed. See file $OUTPUT_FILENAME for the result."
