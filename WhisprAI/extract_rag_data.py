from datasets import load_dataset
import json

# Loading the dataset
dataset = load_dataset("multi_woz_v22", split="train", trust_remote_code=True)

#testing with 500
extracted_dialogs = []
max_pairs = 500
pair_count = 0

for item in dataset:
    turns = item['turns']
    if not isinstance(turns, dict):
        continue
    speakers = turns['speaker']
    utterances = turns['utterance']
    
    for i in range(len(speakers) - 1):
        if speakers[i] == 0 and speakers[i + 1] == 1:  # USER → SYSTEM
            customer = utterances[i].strip()
            agent = utterances[i + 1].strip()
            extracted_dialogs.append({
                "customer": customer,
                "agent": agent,
                "domain": ", ".join(item.get('services', [])) or "unknown"
            })
            pair_count += 1
            if pair_count >= max_pairs:
                break
    if pair_count >= max_pairs:
        break

# Saving to JSON file for extraction
with open("support_rag_dataset.json", "w", encoding="utf-8") as f:
    json.dump(extracted_dialogs, f, indent=2, ensure_ascii=False)

print("✅ Saved 500 conversation pairs to support_rag_dataset.json")
