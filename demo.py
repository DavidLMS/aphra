"""
Demo script for translating a markdown file using the Aphra package.
"""

from aphra import translate

def read_markdown_file(file_path):
    """
    Reads the content of a markdown file.

    :param file_path: Path to the markdown file.
    :return: The content of the file as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_translation_to_file(translation, output_file):
    """
    Writes the translation to an output file.

    :param translation: The translated text.
    :param output_file: Path to the output file.
    """
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("# Traducción\n\n")
        file.write(translation)

def main():
    """
    Main function to read, translate, and write the translation of a markdown file.
    """
    source_language = 'Spanish'
    target_language = 'English'
    input_file = 'input.md'
    output_file = 'translated_output.md'
    config_file = 'aphra/config.toml'
    log_calls = True

    # Leer el contenido del archivo markdown
    text = read_markdown_file(input_file)

    # Realizar la traducción
    translation = translate(
        source_language, target_language, text, config_file=config_file, log_calls=log_calls
    )

    # Escribir la traducción en un archivo de salida
    write_translation_to_file(translation, output_file)

    print(f"Traducción completada. Ver archivo {output_file} para el resultado.")

if __name__ == '__main__':
    main()
