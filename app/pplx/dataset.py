import cohere
import json

# Open the JSON file and load data
with open('../crawler/backup/chatbot.laptop.json', 'r') as json_file:
  data = json.load(json_file)

# Open the JSONL file in write mode
with open('../crawler/backup/chatbot.laptop.jsonl', 'w') as jsonl_file:
  for entry in data:
    # Ensure each entry has a 'prompt' and 'completion' field
    if 'prompt' in entry and 'completion' in entry:
      # Write each entry as a separate line
      jsonl_file.write(json.dumps(entry) + '\n')

co = cohere.Client('ZdmchLQ5VOe6SOLqVR5JJcqOGCyq2KzBWC4f6bOK')

# upload a dataset
my_dataset = co.create_dataset(
  name="langverse-v1-dataset",
  data=open("../crawler/backup/chatbot.laptop.jsonl", "rb"),
  dataset_type="prompt-completion-finetune-input")

# wait for validation to complete
my_dataset.await_validation()

print(my_dataset)