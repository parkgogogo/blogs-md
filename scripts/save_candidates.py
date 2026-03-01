import json

# Read and parse the file
with open('data/hn_new_articles.json', 'r') as f:
    content = f.read()

# Find the JSON array (starts with [)
start_idx = content.find('[')
if start_idx != -1:
    articles = json.loads(content[start_idx:])
    candidates = articles[:60]
    
    with open('data/candidates_60.json', 'w') as f:
        json.dump(candidates, f, indent=2)
    
    print(f'Saved {len(candidates)} candidates to data/candidates_60.json')
else:
    print('No JSON array found')
