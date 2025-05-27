from datasets import load_dataset

# Loading the MultiWOZ v2.2 dataset which is legally allowed to use and complies with hackathon rules
dataset = load_dataset("multi_woz_v22", split="train", trust_remote_code=True)

# Show 1 sample from the dataset to see
print(dataset[0])
