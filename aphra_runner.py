"""
Command-line runner for Aphra translation system.

This module provides a command-line interface to the Aphra translation
functionality, allowing batch processing of text files.

Usage:
    # New style (flags):
    python aphra_runner.py -c config.toml -s Spanish -t English -i input.md -o output.md -w short_article

    # Legacy style (positional, backwards-compatible):
    python aphra_runner.py config.toml Spanish English input.md output.md [workflow]
"""
import sys
import argparse
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


def parse_args():
    """
    Parse command-line arguments supporting both flag-based and legacy positional styles.

    Returns:
        argparse.Namespace with config, source, target, input, output, workflow
    """
    # Legacy mode: first arg doesn't start with '-' → positional style
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        parser = argparse.ArgumentParser(
            description="Aphra translation runner (legacy positional mode)"
        )
        parser.add_argument('config', help="Path to config file (e.g. config.toml)")
        parser.add_argument('source', help="Source language (e.g. Spanish)")
        parser.add_argument('target', help="Target language (e.g. English)")
        parser.add_argument('input', help="Input file path")
        parser.add_argument('output', help="Output file path")
        parser.add_argument('workflow', nargs='?', default=None, help="Workflow name (optional)")
        return parser.parse_args()

    # New flag-based mode
    parser = argparse.ArgumentParser(
        description="Aphra translation runner"
    )
    parser.add_argument('-c', '--config', required=True, help="Path to config file (e.g. config.toml)")
    parser.add_argument('-s', '--source', required=True, help="Source language (e.g. Spanish)")
    parser.add_argument('-t', '--target', required=True, help="Target language (e.g. English)")
    parser.add_argument('-i', '--input', required=True, help="Input file path")
    parser.add_argument('-o', '--output', required=True, help="Output file path")
    parser.add_argument('-w', '--workflow', default=None, help="Workflow name (optional)")
    return parser.parse_args()


def main():
    """
    Main entry point for command-line translation.
    """
    args = parse_args()

    config_file = decode_path(args.config)
    input_file = decode_path(args.input)
    output_file = decode_path(args.output)

    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    translated_text = translate(
        source_language=args.source,
        target_language=args.target,
        text=text,
        config_file=config_file,
        workflow=args.workflow
    )

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(translated_text)


if __name__ == "__main__":
    main()
