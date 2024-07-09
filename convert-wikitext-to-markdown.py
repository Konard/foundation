import mwparserfromhell

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

# # Example usage
# wikitext = """
# ==Heading==
# This is a ''sample'' wikitext with an [[internal link]] and an [http://example.com external link].
# """
# markdown = convert_wikitext_to_markdown(wikitext)
# print(markdown)