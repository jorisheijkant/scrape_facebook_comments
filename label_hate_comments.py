import sys
import json
import csv
from openai import OpenAI

api_key = ""
rows_to_label = []
csv_path = "output.csv"

try:
    with open("secrets.json", "r") as secrets_file:
        secrets_json = json.load(secrets_file)
        print(secrets_json)
        if secrets_json["aimlapi_key"]:
            api_key = secrets_json["aimlapi_key"]
except Exception as e:
    print(f"Key could not be loaded. Are you sure you created your secrets.json file correctly? {e}")
    sys.exit()

base_url = "https://api.aimlapi.com/v1"
api = OpenAI(api_key=api_key, base_url=base_url)

try:
    with open(csv_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for index, row in enumerate(csv_reader):
            if index > 0:
                rows_to_label.append(row)
except Exception as e:
    print(f"Could not read the csv file. Did you scrape and extract all the files correctly? See README for instructions. {e}")
    sys.exit()


total_rows = len(rows_to_label)
labeled_rows = []
limit = 1000 # Adjust this to include all rows but test with a low amount
print_labeled_rows = True
print(f"Total rows: {total_rows}")

system_prompt = """
Je bent een bot die beoordeelt of reacties op sociale media racistisch zijn of niet.
Je krijgt zometeen een reactie, waarbij je een oordeel geeft of de reactie racistisch is.
Je geeft alleen FALSE (bij een niet racistische reactie) of TRUE (bij een wel racistische reactie) terug. 
"""

def limit_text_by_word_count(text, max_words):
    words = text.split()
    limited_text = ' '.join(words[:max_words])
    return limited_text

for index, row in enumerate(rows_to_label):
    parsed_row = row
    print(f"Now labeling row {index}/{len(rows_to_label)}")
    if index < limit:
        question_text = row[2]
        limited_text = limit_text_by_word_count(question_text, 1000) # Just so we don't go over the token limit

        try:
            completion = api.chat.completions.create(
                model="google/gemma-2-27b-it",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": limited_text},
                ],
                temperature=0.25,
                max_tokens=20
            )

            response = completion.choices[0].message.content

            parsed_row.append(response)
            labeled_rows.append(parsed_row)
        except Exception as e:
            print(f"Labeling row {index} failed: {e}")

with open("labeled_output.csv", "w") as csv_output_file:
    csv_writer = csv.writer(csv_output_file)
    csv_writer.writerow(["article", "name", "comment", "is_racist"])
    for row in labeled_rows:
        csv_writer.writerow([row[0], row[1], row[2], row[3]])