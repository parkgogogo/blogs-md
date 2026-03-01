import json
import glob
from datetime import datetime

all_ratings = []

# Read today's rating files (1-6)
for i in range(1, 7):
    try:
        with open(f'data/ratings_batch_{i}.json', 'r') as f:
            batch = json.load(f)
            all_ratings.extend(batch)
            print(f'Loaded batch {i}: {len(batch)} articles')
    except Exception as e:
        print(f'Error loading batch {i}: {e}')

print(f'\nTotal articles rated: {len(all_ratings)}')

# Sort by rating (descending), then filter for 8+
sorted_ratings = sorted(all_ratings, key=lambda x: x.get('rating', 0), reverse=True)
top_articles = [a for a in sorted_ratings if a.get('rating', 0) >= 8][:12]

print(f'\nTop 12 articles (rating 8+):')
for i, article in enumerate(top_articles, 1):
    print(f"{i}. [{article['rating']}] {article['title_en'][:60]}... ({article['category']})")

# Save top 12 for translation
with open('data/top_12_for_translation.json', 'w') as f:
    json.dump(top_articles, f, indent=2)

print(f'\nSaved top {len(top_articles)} articles to data/top_12_for_translation.json')
