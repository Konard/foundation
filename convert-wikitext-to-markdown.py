import mwparserfromhell
import sys

def convert_wikitext_to_markdown(wikitext):
    wikicode = mwparserfromhell.parse(wikitext)
    markdown = str(wikicode)

    # Convert links
    for link in wikicode.filter_wikilinks():
        target = link.title.strip_code()
        if '://' in target:  # External link
            text = link.text.strip_code() if link.text else target
            markdown = markdown.replace(str(link), f'[{text}]({target})')
        else:  # Internal link
            url = f'https://en.wikipedia.org/wiki/{target.replace(" ", "_")}'
            text = link.text.strip_code() if link.text else target
            markdown = markdown.replace(str(link), f'[{text}]({url})')

    # Convert headings
    markdown = markdown.replace("===", "###")
    markdown = markdown.replace("==", "##")
    markdown = markdown.replace("=", "#")

    # Convert bold and italic
    markdown = markdown.replace("'''", "**")
    markdown = markdown.replace("''", "*")

    return markdown

def main(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        wikitext = file.read()
    
    markdown = convert_wikitext_to_markdown(wikitext)
    
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(markdown)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_wikitext_file> <output_markdown_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    main(input_file, output_file)
