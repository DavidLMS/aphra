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

# Read the content of the input file
TEXT=$(cat "$INPUT_FILE")

# Execute the translation
TRANSLATION=$(python -c "
from aphra import translate
result = translate('$SOURCE_LANGUAGE', '$TARGET_LANGUAGE', '''$TEXT''', config_file='config.toml')
print(result)
")

# Save the translation to the output file
echo "$TRANSLATION" > "$OUTPUT_FILE"

echo "Translation completed. See file $OUTPUT_FILE for the result."