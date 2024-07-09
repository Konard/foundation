import wikipediaapi

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"

def get_wikitext(page_name):
    wiki_wiki = wikipediaapi.Wikipedia(user_agent, 'en')

    page = wiki_wiki.page(page_name)
    if page.exists():
        return page.text
    else:
        return None

page_name = "Python (programming language)"
wikitext = get_wikitext(page_name)

if wikitext:
    print(wikitext)
else:
    print(f"The page '{page_name}' does not exist.")