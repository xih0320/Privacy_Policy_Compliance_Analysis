import json
import csv



PERMISSION_KEYWORDS = {
    "Steps": {
        "verbs": [
            "collect", "gather", "obtain", "receive", "record", "store", "solicit",
            "retain", "hold", "keep", "possess", "save", "withhold",
            "share", "disclose", "transfer", "sell", "distribute", "transmit",
            "track", "monitor", "access"
        ],
        "data_keywords": [
            "step", "steps", "step count", "pedometer",
            "walking", "footstep", "physical activity", "activity data"
        ]
    },
    "Distance": {
        "verbs": [
            "collect", "gather", "obtain", "receive", "record", "store", "solicit",
            "retain", "hold", "keep", "possess", "save", "withhold",
            "share", "disclose", "transfer", "sell", "distribute", "transmit",
            "track", "monitor", "access"
        ],
        "data_keywords": [
            "distance", "location", "gps", "route",
            "travel", "movement", "geo"
        ]
    },
    "Heart rate": {
        "verbs": [
            "collect", "gather", "obtain", "receive", "record", "store", "solicit",
            "retain", "hold", "keep", "possess", "save", "withhold",
            "share", "disclose", "transfer", "sell", "distribute", "transmit",
            "track", "monitor", "access"
        ],
        "data_keywords": [
            "heart rate", "heartrate", "pulse", "bpm", "cardiac", "heart"
        ]
    },
    "Calories": {
        "verbs": [
            "collect", "gather", "obtain", "receive", "record", "store", "solicit",
            "retain", "hold", "keep", "possess", "save", "withhold",
            "share", "disclose", "transfer", "sell", "distribute", "transmit",
            "track", "monitor", "access"
        ],
        "data_keywords": [
            "calorie", "calories", "energy", "burn", "dietary", "nutrition"
        ]
    },
    "Sleep": {
        "verbs": [
            "collect", "gather", "obtain", "receive", "record", "store", "solicit",
            "retain", "hold", "keep", "possess", "save", "withhold",
            "share", "disclose", "transfer", "sell", "distribute", "transmit",
            "track", "monitor", "access"
        ],
        "data_keywords": [
            "sleep", "sleeping", "rest", "bedtime", "wake"
        ]
    },
    "Weight": {
        "verbs": [
            "collect", "gather", "obtain", "receive", "record", "store", "solicit",
            "retain", "hold", "keep", "possess", "save", "withhold",
            "share", "disclose", "transfer", "sell", "distribute", "transmit",
            "track", "monitor", "access"
        ],
        "data_keywords": [
            "weight", "bmi", "body mass", "body weight"
        ]
    }
}

NEGATION_WORDS = [
    "not", "never", "no", "without", "neither", "nor",
    "don't", "doesn't", "won't", "cannot", "can't"
]



def check_permission_in_policy(pp_text, permission):
    """
    Check whether a privacy policy mentions collecting a specific type of data.
    Triple matching per sentence:
      1. Sentence contains a verb (collect / store / share / etc.)
      2. Sentence contains a data keyword (steps / heart rate / etc.)
      3. Sentence does NOT contain a negation word
    All three must be true -> policy is considered to mention this permission.
    """
    if permission not in PERMISSION_KEYWORDS:
        return False

    pp_lower = pp_text.lower()
    verbs = PERMISSION_KEYWORDS[permission]["verbs"]
    data_keywords = PERMISSION_KEYWORDS[permission]["data_keywords"]
    sentences = pp_lower.replace("\n", " ").split(".")

    for sentence in sentences:
        has_verb = any(verb in sentence for verb in verbs)
        has_data = any(kw in sentence for kw in data_keywords)
        has_negation = any(neg in sentence for neg in NEGATION_WORDS)

        if has_verb and has_data and not has_negation:
            return True

    return False



def analyze_record(record):
    """
    Find inconsistencies between declared permissions and policy mentions.
    Type 1: Declared permission X but policy never mentions it -> compliance risk
    Type 2: Policy mentions data Y but permission was not declared -> reverse inconsistency
    """
    pp_text = record.get("pp", "")
    declared = record.get("declared_permission", [])

    pp_mentions = [
        perm for perm in PERMISSION_KEYWORDS
        if check_permission_in_policy(pp_text, perm)
    ]

    issues = []
    for perm in declared:
        if perm not in pp_mentions:
            issues.append(f"Declared '{perm}' permission but policy does not mention it")
    for perm in pp_mentions:
        if perm not in declared:
            issues.append(f"Policy mentions '{perm}' but permission was not declared")

    return pp_mentions, issues



all_data = []
for filename in ["1.jsonl", "2.jsonl", "3.jsonl"]:
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                all_data.append(json.loads(line))

print(f"Loaded {len(all_data)} records")


results = []
for record in all_data:
    pp_mentions, issues = analyze_record(record)
    results.append({
        "packagename": record["packagename"],
        "declared_permission": " | ".join(record.get("declared_permission", [])),
        "pp_mentions": " | ".join(pp_mentions) if pp_mentions else "None",
        "has_issue": "YES" if issues else "NO",
        "issues": " | ".join(issues) if issues else "None"
    })


with open("output_keyword.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["packagename", "declared_permission", "pp_mentions", "has_issue", "issues"]
    )
    writer.writeheader()
    writer.writerows(results)

print("Results saved to output_keyword.csv")


total = len(results)
has_issue_count = sum(1 for r in results if r["has_issue"] == "YES")
no_issue_count = total - has_issue_count

print()
print("=== SUMMARY ===")
print(f"Total records:          {total}")
print(f"Compliance risk (YES):  {has_issue_count} ({has_issue_count/total*100:.1f}%)")
print(f"No issue (NO):          {no_issue_count} ({no_issue_count/total*100:.1f}%)")

print()
print("=== EXAMPLE CASES WITH ISSUES (first 5) ===")
count = 0
for r in results:
    if r["has_issue"] == "YES" and count < 5:
        print(f"App: {r['packagename']}")
        print(f"  Declared permissions : {r['declared_permission']}")
        print(f"  Policy mentions      : {r['pp_mentions']}")
        print(f"  Issues               : {r['issues']}")
        print()
        count += 1
