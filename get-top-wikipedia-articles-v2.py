import requests
import pandas as pd
import time

def get_top_articles(limit=1000):
    url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/2024/01/01'
    response = requests.get(url)
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
    response = requests.get(url)
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
    top_articles = get_top_articles()
    
    for article in top_articles:
        title = article['title']
        translations = get_translations(title)
        article['translations'] = translations
        time.sleep(0.1)  # To prevent hitting the API rate limit
    
    df = pd.DataFrame(top_articles)
    df.to_csv('top_1000_wikipedia_articles.csv', index=False)
    print("Top 1000 Wikipedia articles and their translations have been saved to 'top_1000_wikipedia_articles.csv'.")

if __name__ == "__main__":
    main()