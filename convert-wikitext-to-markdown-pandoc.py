#!/usr/bin/env python3
"""
Improved wikitext to markdown converter using Pandoc via pypandoc.
This addresses the issue request to "Try panda" (referring to Pandoc).
"""

import pypandoc
import sys
import os


def convert_wikitext_to_markdown_pandoc(wikitext):
    """
    Convert wikitext to markdown using Pandoc.

    Args:
        wikitext (str): The wikitext content to convert

    Returns:
        str: The converted markdown content
    """
    try:
        # Use pypandoc to convert from mediawiki format to markdown
        markdown = pypandoc.convert_text(
            wikitext,
            'markdown',
            format='mediawiki',
            extra_args=['--wrap=none']  # Prevent line wrapping
        )
        return markdown
    except Exception as e:
        print(f"Error during conversion: {e}", file=sys.stderr)
        return None


def main():
    """Main function to handle command line arguments and file operations."""
    if len(sys.argv) != 3:
        print("Usage: python convert-wikitext-to-markdown-pandoc.py <input_wikitext_file> <output_markdown_file>")
        print("Example: python convert-wikitext-to-markdown-pandoc.py sample.wikitext output.md")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.", file=sys.stderr)
        sys.exit(1)

    try:
        # Read the wikitext file
        with open(input_file, 'r', encoding='utf-8') as f:
            wikitext = f.read()

        print(f"Converting '{input_file}' to markdown using Pandoc...")

        # Convert using Pandoc
        markdown = convert_wikitext_to_markdown_pandoc(wikitext)

        if markdown is None:
            print("Conversion failed.", file=sys.stderr)
            sys.exit(1)

        # Write the markdown file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown)

        print(f"Successfully converted to '{output_file}'")
        print(f"Input size: {len(wikitext)} characters")
        print(f"Output size: {len(markdown)} characters")

    except IOError as e:
        print(f"File I/O error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()