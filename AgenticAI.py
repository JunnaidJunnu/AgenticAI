import requests
from bs4 import BeautifulSoup
import json

def fetch_dev_to_articles():
    url = "https://dev.to/api/articles?top=7"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

def fetch_hacker_news():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(url)
    if response.status_code == 200:
        top_story_ids = response.json()[:10]
        stories = []
        for story_id in top_story_ids:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_response = requests.get(story_url)
            if story_response.status_code == 200:
                stories.append(story_response.json())
        return stories
    return []

def fetch_github_trending():
    url = "https://github.com/trending"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        repos = soup.find_all('h1', class_='h3 lh-condensed')
        trending_repos = [repo.text.strip() for repo in repos[:5]]
        return trending_repos
    return []

def summarize_articles(articles):
    summaries = []
    for article in articles:
        summaries.append(f"{article['title']} - {article['url']}")
    return summaries

if __name__ == "__main__":
    dev_to_articles = fetch_dev_to_articles()
    hacker_news_articles = fetch_hacker_news()
    github_trending = fetch_github_trending()

    print("Top DEV.to Articles:")
    print(json.dumps(summarize_articles(dev_to_articles), indent=2))

    print("\nTop Hacker News Stories:")
    print(json.dumps(summarize_articles(hacker_news_articles), indent=2))

    print("\nTrending GitHub Repositories:")
    print(json.dumps(github_trending, indent=2))
