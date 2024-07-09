import wikipedia

def get_wikitext(page_name):
    try:
        # Fetch the page content
        page_content = wikipedia.page(page_name).content
        return page_content
    except wikipedia.exceptions.PageError:
        return None
    except wikipedia.exceptions.DisambiguationError as e:
        return f"The page '{page_name}' is a disambiguation page. Options are: {e.options}"

page_name = "Python (programming language)"
wikitext = get_wikitext(page_name)

if wikitext:
    print(wikitext)
else:
    print(f"The page '{page_name}' does not exist or is a disambiguation page.")