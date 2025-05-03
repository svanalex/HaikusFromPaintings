import requests
import random
from .config import CATEGORY_QUERIES
from datetime import datetime, timedelta

def determine_date_range(use_single_day=True):
    today = datetime.today().date()
    if use_single_day:
        return today.isoformat(), today.isoformat()
    else:
        end_date = today
        start_date = today - timedelta(days=14)
        return start_date.isoformat(), end_date.isoformat()

def get_newsapi_articles(api_key, category=None, start_date=None, end_date=None, use_everything=False):
    if use_everything and start_date and end_date:
        query = CATEGORY_QUERIES.get(category, "news")
        url = (
            f"https://newsapi.org/v2/everything?q={query}"
            f"&from={start_date}&to={end_date}&sortBy=popularity&pageSize=20&language=en&apiKey={api_key}"
        )
    else:
        #print(category)
        url = (
            f"https://newsapi.org/v2/top-headlines?category={category}&country=us&pageSize=15&apiKey={api_key}"
        )
        #print("This was reached.")

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch news for {category}")
        return []
    return response.json().get("articles", [])

def get_weighted_articles(api_key, profile, total_articles, start_date=None, end_date=None, use_everything=False):
    category_weights = profile["category_weights"]
    categories = list(category_weights.keys())
    #print(categories)

    # Normalize weights
    total_weight = sum(category_weights.values())
    normalized_weights = {
        cat: weight / total_weight for cat, weight in category_weights.items()
    }

    # Initial distribution
    article_distribution = {
        cat: max(1, round(total_articles * normalized_weights[cat]))
        for cat in categories
    }

    # Adjust to ensure total adds up to exactly `total_articles`
    while sum(article_distribution.values()) > total_articles:
        max_cat = max(article_distribution, key=article_distribution.get)
        if article_distribution[max_cat] > 1:
            article_distribution[max_cat] -= 1

    while sum(article_distribution.values()) < total_articles:
        min_cat = min(article_distribution, key=article_distribution.get)
        article_distribution[min_cat] += 1

    # Fetch and aggregate articles
    seen_urls = set()
    all_articles = []
    for cat in categories:
        print(f"\n Reading {cat.upper()} news (up to {article_distribution[cat]} articles)...")
        fetched = get_newsapi_articles(api_key, category=cat, start_date=start_date, end_date=end_date, use_everything=use_everything)
        usable = []

        for article in fetched:
            if len(usable) >= article_distribution[cat]:
                break  # Stop when we reach desired count for this category

            url = article.get("url")
            description = article.get("description") or ""
            if not description:
                print(f"Skipping article with no description: {article.get('title', 'No title')}")
                continue

            if url and url not in seen_urls and len(description.split()) > 5:
                seen_urls.add(url)
                usable.append({
                    "category": cat,
                    "url": url,
                    "description": description,
                    "title": article.get("title"),
                    "publishedAt": article.get("publishedAt")
                })

        all_articles.extend(usable)

    return all_articles




