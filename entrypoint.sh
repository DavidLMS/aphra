#!/bin/bash

# Verify that the correct number of arguments have been passed
if [ "$#" -ne 4 ];then
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

# Read the content of the input file into a variable
TEXT=$(cat "$INPUT_FILE")

# Escaping the content to ensure it's safely passed into the Python command
ESCAPED_TEXT=$(printf '%s\n' "$TEXT" | sed -e 's/"/\\"/g' -e 's/\$/\\$/g')

# Prepare the Python command with the actual content of the ESCAPED_TEXT variable
PYTHON_COMMAND=$(cat <<EOF
from aphra import translate
result = translate('$SOURCE_LANGUAGE', '$TARGET_LANGUAGE', "$ESCAPED_TEXT", config_file='config.toml')
print(result)
EOF
)

# Execute the translation
TRANSLATION=$(python -c "$PYTHON_COMMAND")

# Save the translation to the output file on the host
echo "$TRANSLATION" > "$OUTPUT_FILE"

# Output a message with the output file name
OUTPUT_FILENAME=$(basename "$OUTPUT_FILE")
echo "Translation completed. See file $OUTPUT_FILENAME for the result."
