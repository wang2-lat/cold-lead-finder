import praw
import requests
from typing import List, Dict
from time import sleep

class RedditScraper:
    def __init__(self, client_id: str, client_secret: str):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent="cold-lead-finder/0.1"
        )
    
    def search(self, keywords: List[str], limit: int = 50) -> List[Dict]:
        posts = []
        query = " OR ".join(keywords)
        
        try:
            for submission in self.reddit.subreddit("all").search(query, limit=limit, sort="new"):
                posts.append({
                    "platform": "reddit",
                    "author": str(submission.author),
                    "title": submission.title,
                    "content": submission.selftext,
                    "url": f"https://reddit.com{submission.permalink}",
                    "score": submission.score
                })
                sleep(0.1)  # Rate limiting
        except Exception as e:
            print(f"Reddit error: {e}")
        
        return posts

class HNScraper:
    def __init__(self):
        self.api_url = "https://hn.algolia.com/api/v1/search"
    
    def search(self, keywords: List[str], limit: int = 50) -> List[Dict]:
        posts = []
        
        for keyword in keywords:
            try:
                response = requests.get(
                    self.api_url,
                    params={"query": keyword, "tags": "story", "hitsPerPage": limit}
                )
                response.raise_for_status()
                data = response.json()
                
                for hit in data.get("hits", []):
                    posts.append({
                        "platform": "hackernews",
                        "author": hit.get("author", "unknown"),
                        "title": hit.get("title", ""),
                        "content": hit.get("story_text", ""),
                        "url": hit.get("url", f"https://news.ycombinator.com/item?id={hit.get('objectID')}"),
                        "score": hit.get("points", 0)
                    })
                
                sleep(0.5)  # Rate limiting
            except Exception as e:
                print(f"HN error: {e}")
        
        return posts[:limit]