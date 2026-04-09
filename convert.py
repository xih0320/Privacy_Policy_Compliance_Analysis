import json
import csv
import os


all_data = []
for filename in ['1.jsonl', '2.jsonl', '3.jsonl']:
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                all_data.append(json.loads(line))

print(f"共读取 {len(all_data)} 条记录")


with open('output.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['packagename', 'pp', 'declared_permission'])
    for d in all_data:
        writer.writerow([
            d.get('packagename', ''),
            d.get('pp', ''),
            ', '.join(d.get('declared_permission', []))
        ])

print("CSV :output.csv")


cards = ''
for d in all_data:
    name = d.get('packagename', 'Unknown')
    pp = d.get('pp', '').replace('\n', '<br>')
    perms = d.get('declared_permission', [])
    perm_tags = ''.join(f'<span class="tag">{p}</span>' for p in perms)

    cards += f'''
    <div class="card">
        <h2>{name}</h2>
        <div class="perms"><strong>Permissions：</strong>{perm_tags if perm_tags else '<span class="none">None</span>'}</div>
        <details>
            <summary>查看隐私政策全文</summary>
            <div class="pp">{pp}</div>
        </details>
    </div>
    '''

html = f'''<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>Privacy Policy Viewer</title>
<style>
  body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; background: #f5f5f5; }}
  h1 {{ color: #333; }}
  .card {{ background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }}
  h2 {{ margin: 0 0 10px; color: #1a73e8; font-size: 16px; }}
  .perms {{ margin-bottom: 10px; }}
  .tag {{ background: #e8f0fe; color: #1a73e8; padding: 2px 8px; border-radius: 12px; margin-right: 6px; font-size: 13px; }}
  .none {{ color: #999; font-size: 13px; }}
  details summary {{ cursor: pointer; color: #555; font-size: 14px; }}
  .pp {{ margin-top: 10px; font-size: 13px; color: #444; line-height: 1.6; max-height: 300px; overflow-y: auto; border-top: 1px solid #eee; padding-top: 10px; }}
</style>
</head>
<body>
<h1>Privacy Policy Viewer（共 {len(all_data)} 条）</h1>
{cards}
</body>
</html>'''

with open('output.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML 已生成：output.html")
