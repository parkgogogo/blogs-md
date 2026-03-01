import json

# Read candidates
with open('data/candidates_60.json', 'r') as f:
    candidates = json.load(f)

# Split into 6 batches of 5 articles each
batch_size = 5
num_batches = 6

for i in range(num_batches):
    start = i * batch_size
    end = start + batch_size
    batch = candidates[start:end]
    
    batch_file = f'data/rating_batch_{i+1}.json'
    with open(batch_file, 'w') as f:
        json.dump(batch, f, indent=2)
    
    print(f'Batch {i+1}: articles {start+1}-{min(end, len(candidates))} -> {batch_file}')

print(f'\nTotal: {len(candidates)} articles split into {num_batches} batches')
