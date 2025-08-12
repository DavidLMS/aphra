"""
Command-line runner for Aphra translation system.

This module provides a command-line interface to the Aphra translation
functionality, allowing batch processing of text files.
"""
import sys
import urllib.parse
from aphra import translate

def decode_path(path):
    """
    Decode URL-encoded file paths.
    
    Args:
        path: URL-encoded file path string
        
    Returns:
        str: Decoded file path
    """
    return urllib.parse.unquote(path)

def main():
    """
    Main entry point for command-line translation.
    
    Processes command-line arguments and performs translation using Aphra.
    Expected arguments: config_file source_lang target_lang input_file output_file
    """
    config_file = decode_path(sys.argv[1])
    source_language = sys.argv[2]
    target_language = sys.argv[3]
    input_file = decode_path(sys.argv[4])
    output_file = decode_path(sys.argv[5])

    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    translated_text = translate(
        source_language=source_language,
        target_language=target_language,
        text=text,
        config_file=config_file
    )

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(translated_text)

if __name__ == "__main__":
    main()
