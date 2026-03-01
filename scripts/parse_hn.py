#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.10"
# ///

import json
import xml.etree.ElementTree as ET
import re
from datetime import datetime
import sys

# Parse HN RSS
rss_content = sys.stdin.read()
root = ET.fromstring(rss_content)

articles = []
for item in root.findall('.//item'):
    title = item.find('title').text if item.find('title') is not None else ''
    link = item.find('link').text if item.find('link') is not None else ''
    pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
    comments = item.find('comments').text if item.find('comments') is not None else ''
    
    articles.append({
        'title': title,
        'url': link,
        'pubDate': pub_date,
        'comments': comments
    })

# Load processed URLs
try:
    with open('data/processed_urls.json', 'r') as f:
        processed = json.load(f)
except:
    processed = []

processed_set = set(processed)

# Filter out processed
new_articles = [a for a in articles if a['url'] not in processed_set]

print(json.dumps(new_articles, indent=2))
print(f"\nTotal: {len(articles)}, New: {len(new_articles)}, Processed: {len(processed)}", file=sys.stderr)
