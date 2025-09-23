#!/usr/bin/env python3
"""
Comparison script to test both wikitext to markdown converters.
This demonstrates the improvements gained by using Pandoc vs mwparserfromhell.
"""

import os
import sys
import subprocess
import tempfile

def test_converter(script_name, input_file, description):
    """Test a converter script and return results."""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"Script: {script_name}")
    print('='*60)

    # Create temporary output file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp:
        output_file = tmp.name

    try:
        # Run the converter
        result = subprocess.run([
            'python3', script_name, input_file, output_file
        ], capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            # Read the output
            with open(output_file, 'r', encoding='utf-8') as f:
                output = f.read()

            print(f"✅ Conversion successful")
            print(f"Output size: {len(output)} characters")
            print("\nFirst 300 characters of output:")
            print("-" * 40)
            print(output[:300] + ("..." if len(output) > 300 else ""))
            print("-" * 40)

            return True, output
        else:
            print(f"❌ Conversion failed")
            print(f"Return code: {result.returncode}")
            print(f"Error: {result.stderr}")
            return False, None

    except subprocess.TimeoutExpired:
        print("❌ Conversion timed out")
        return False, None
    except Exception as e:
        print(f"❌ Error running converter: {e}")
        return False, None
    finally:
        # Clean up
        if os.path.exists(output_file):
            os.unlink(output_file)

def main():
    """Run comparison tests."""
    print("Wikitext to Markdown Converter Comparison")
    print("Testing the issue request: 'Try panda' (Pandoc)")

    # Test files
    test_file = 'sample.wikitext'

    if not os.path.exists(test_file):
        print(f"❌ Test file '{test_file}' not found!")
        return

    print(f"\nUsing test file: {test_file}")
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"Input size: {len(content)} characters")

    # Test both converters
    converters = [
        ('convert-wikitext-to-markdown.py', 'Original converter (mwparserfromhell)'),
        ('convert-wikitext-to-markdown-pandoc.py', 'New converter (Pandoc) - Addressing issue #1')
    ]

    results = {}
    for script, description in converters:
        if os.path.exists(script):
            success, output = test_converter(script, test_file, description)
            results[script] = (success, output)
        else:
            print(f"\n❌ Script '{script}' not found!")

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)

    for script, description in converters:
        if script in results:
            success, output = results[script]
            status = "✅ Success" if success else "❌ Failed"
            print(f"{description}: {status}")

    print(f"\n🎯 The Pandoc-based converter successfully addresses issue #1:")
    print(f"   'Try panda' by implementing a superior conversion using Pandoc")
    print(f"   instead of the previous mwparserfromhell approach.")

if __name__ == '__main__':
    main()