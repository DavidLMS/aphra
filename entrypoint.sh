#!/bin/bash

# Verify that the correct number of arguments have been passed
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <source_language> <target_language> <input_file> <output_file>"
    exit 1
fi

# Assign arguments to variables
SOURCE_LANGUAGE=$1
TARGET_LANGUAGE=$2
INPUT_FILE=$3
OUTPUT_FILE=$4

# Ensure the input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Input file $INPUT_FILE does not exist."
    exit 1
fi

# Execute the translation
TRANSLATION=$(python -c "
from aphra import translate
with open('$INPUT_FILE', 'r') as file:
    text = file.read()
result = translate('$SOURCE_LANGUAGE', '$TARGET_LANGUAGE', '''$text''', config_file='config.toml')
print(result)
")

# Save the translation to the output file on the host
echo "$TRANSLATION" > "$OUTPUT_FILE"

# Output a message with the output file name
OUTPUT_FILENAME=$(basename "$OUTPUT_FILE")
echo "Translation completed. See file $OUTPUT_FILENAME for the result."
