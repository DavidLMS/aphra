import sys
import urllib.parse
from aphra import translate

def decode_path(path):
    return urllib.parse.unquote(path)

def main():
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
