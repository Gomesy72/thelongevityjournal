import os

def fix_special_chars(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace special characters with HTML entities
    replacements = {
        '\u2014': '&mdash;',  # em dash
        '\u2013': '&ndash;',  # en dash
        '\u201c': '&ldquo;',  # left double quote
        '\u201d': '&rdquo;',  # right double quote
        '\u2018': '&lsquo;',  # left single quote
        '\u2019': '&rsquo;',  # right single quote
        '\u2026': '&hellip;', # ellipsis
        '\u2190': '&larr;',   # left arrow
        '\u2192': '&rarr;',   # right arrow
        '\u00b7': '&middot;', # middle dot
        '\u2022': '&bull;',   # bullet
    }
    
    count = 0
    for char, entity in replacements.items():
        if char in content:
            occurrences = content.count(char)
            content = content.replace(char, entity)
            if occurrences > 0:
                print(f"  Replaced {occurrences} occurrences")
                count += occurrences
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Total in {filename}: {count}")
    return count

files = [
    'sleep-optimization-20260529.html',
    'ai-drug-discovery-20260529.html',
    'trt-longevity-20260529.html',
    'apoe4-20260529.html'
]

total = 0
for file in files:
    if os.path.exists(file):
        print(f"\nProcessing {file}...")
        total += fix_special_chars(file)

print(f"\nDone! Total: {total}")
