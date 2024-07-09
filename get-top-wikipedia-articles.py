import requests
import pandas as pd
import time
import json

# Define a user-agent string that mimics a typical browser
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

def get_top_articles(limit=1000):
    url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/2024/01/01'
    headers = {'User-Agent': USER_AGENT}
    response = requests.get(url, headers=headers)
    try:
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []
    except ValueError as e:
        print(f"JSON decode error: {e}")
        return []
    
    articles = []
    for item in data.get('items', [])[0].get('articles', [])[:limit]:
        articles.append({'title': item['article'], 'views': item['views']})
    
    return articles

def get_translations(title):
    url = f'https://en.wikipedia.org/w/api.php?action=query&prop=langlinks&titles={title}&lllimit=500&format=json'
    headers = {'User-Agent': USER_AGENT}
    response = requests.get(url, headers=headers)
    try:
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {}
    except ValueError as e:
        print(f"JSON decode error: {e}")
        return {}
    
    translations = {}
    pages = data.get('query', {}).get('pages', {})
    for page_id in pages:
        if 'langlinks' in pages[page_id]:
            for langlink in pages[page_id]['langlinks']:
                translations[langlink['lang']] = langlink['*']
    
    return translations

def main():
    limit = 5  # Adjust this value to get a different number of top articles
    top_articles = get_top_articles(limit)
    
    for article in top_articles:
        title = article['title']
        translations = get_translations(title)
        article['translations'] = translations
        time.sleep(0.1)  # To prevent hitting the API rate limit
    
    # Save the results to a JSON file
    with open(f'top_{limit}_wikipedia_articles.json', 'w', encoding='utf-8') as f:
        json.dump(top_articles, f, ensure_ascii=False, indent=4)
    
    print(f"Top {limit} Wikipedia articles and their translations have been saved to 'top_{limit}_wikipedia_articles.json'.")

if __name__ == "__main__":
    main()