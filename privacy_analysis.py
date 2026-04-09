import json
import csv
import time
import os
import vertexai
from vertexai.generative_models import GenerativeModel

# Set your GCP project ID as an environment variable:
# export GCP_PROJECT_ID="your-project-id"
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "your-project-id")
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)
model = GenerativeModel("gemini-2.5-flash-lite")

data = []
for filename in ["1.jsonl", "2.jsonl", "3.jsonl"]:
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))

print(f"Loaded {len(data)} records")

def analyze_policy(policy_text, permissions):
    prompt = (
        "You are a privacy compliance expert analyzing mobile app privacy policies.\n"
        "The app declares these health permissions: " + str(permissions) + "\n\n"
        "For each permission, check if the privacy policy mentions collecting this data.\n"
        "Answer YES, NO, or PARTIAL for each permission.\n\n"
        "Privacy Policy:\n" + policy_text[:3000] + "\n\n"
        "Respond in this format for each permission:\n"
        "Permission: [permission name]\n"
        "Status: [YES/NO/PARTIAL]\n"
        "Reason: [one sentence explanation]\n"
        "---\n"
    )
    response = model.generate_content(prompt)
    return response.text

results = []
for i, record in enumerate(data):
    print(f"Processing {i+1}/{len(data)}: {record['packagename']}")
    try:
        analysis = analyze_policy(
            record["pp"],
            record["declared_permission"]
        )
        results.append({
            "packagename": record["packagename"],
            "permissions": str(record["declared_permission"]),
            "analysis": analysis
        })
        time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        continue

with open("output_llm.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f, fieldnames=["packagename", "permissions", "analysis"]
    )
    writer.writeheader()
    writer.writerows(results)

print(f"Done! Processed {len(results)} records. Results saved to output_llm.csv")
