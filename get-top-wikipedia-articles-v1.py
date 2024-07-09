import requests
import pandas as pd

def get_top_articles(limit=1000):
    # URL for the Wikimedia Pageviews API to get the most viewed articles
    url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/2024/01/01'
    response = requests.get(url)
    data = response.json()
    
    articles = []
    for item in data['items'][0]['articles'][:limit]:
        articles.append({'title': item['article'], 'views': item['views']})
    
    return articles

def get_translations(title):
    # URL for the Wikipedia API to get translations of a given article title
    url = f'https://en.wikipedia.org/w/api.php?action=query&prop=langlinks&titles={title}&lllimit=500&format=json'
    response = requests.get(url)
    data = response.json()
    
    translations = {}
    pages = data['query']['pages']
    for page_id in pages:
        if 'langlinks' in pages[page_id]:
            for langlink in pages[page_id]['langlinks']:
                translations[langlink['lang']] = langlink['*']
    
    return translations

def main():
    # Fetch the top articles
    top_articles = get_top_articles()
    
    for article in top_articles:
        title = article['title']
        translations = get_translations(title)
        article['translations'] = translations
    
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(top_articles)
    
    # Save the DataFrame to a CSV file
    df.to_csv('top_1000_wikipedia_articles.csv', index=False)
    print("Top 1000 Wikipedia articles and their translations have been saved to 'top_1000_wikipedia_articles.csv'.")

if __name__ == "__main__":
    main()