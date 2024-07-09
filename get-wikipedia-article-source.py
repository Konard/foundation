import requests

def get_wikitext(page_name):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": page_name,
        "prop": "revisions",
        "rvprop": "content",
        "rvslots": "main",
    }

    response = requests.get(url, params=params)
    data = response.json()
    
    pages = data.get("query", {}).get("pages", {})
    page_id = next(iter(pages))
    page = pages[page_id]
    
    if "revisions" in page:
        return page["revisions"][0]["slots"]["main"]["*"]
    else:
        return None

page_name = "Python (programming language)"
wikitext = get_wikitext(page_name)

if wikitext:
    # Save to a file
    with open("Python_programming_language.wt", "w", encoding="utf-8") as f:
        f.write(wikitext)
else:
    print(f"The page '{page_name}' does not exist.")