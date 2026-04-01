from duckduckgo_search import DDGS
import json

with DDGS() as ddgs:
    query = 'software intern remote'
    print(f'Testing query: {query}')
    results = list(ddgs.text(query, max_results=10))
    if not results:
        print('No results found at all.')
    else:
        for r in results:
            print(f"- {r['title']} | {r['href']}")
