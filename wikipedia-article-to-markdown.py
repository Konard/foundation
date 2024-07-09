import wikipediaapi
import requests
from markdownify import markdownify as md

# Set user agent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"


# Initialize the Wikipedia API with the session
wiki_wiki = wikipediaapi.Wikipedia(user_agent, 'en')

# Get the Wikipedia page
page = wiki_wiki.page('Python (programming language)')

if page.exists():
    # Convert HTML to Markdown
    markdown_content = md(page.text, heading_style="ATX")

    # Save to a file
    with open("Python_programming_language.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print("Article saved as Markdown.")
else:
    print("Page not found.")