import re
import os

def fix_article(filename):
    """Fix article HTML structure, encoding, and mobile compatibility"""
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Replace broken arrow characters with proper HTML entities
    content = content.replace('�+?', '←')
    content = content.replace('�?', '←') 
    content = content.replace('�', '')
    
    # Fix 2: Replace broken emojis
    content = content.replace('??', '')  # Remove broken emoji placeholders
    
    # Fix 3: Fix the back-link to use proper arrow
    content = content.replace('class="back-link"> Back to Latest Issue', 'class="back-link">← Back to Latest Issue')
    
    # Fix 4: Remove duplicate h1 titles (the article-header already has one)
    # Find the article-body and remove the duplicate h1 inside it
    pattern = r'(<article class="article-body">)\s*<h1>.*?</h1>'
    replacement = r'\1'
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Fix 5: Add article-content wrapper around the article-body content for proper styling
    # The article-body should be inside an article-content div
    if 'class="article-content"' not in content:
        content = content.replace(
            '<article class="article-body">',
            '<div class="article-content">\n<article class="article-body">'
        )
        # Close the article-content div before closing article-body
        content = content.replace(
            '</article>\n    </div>\n</body>',
            '</article>\n</div>\n    </div>\n</body>'
        )
    
    # Fix 6: Remove empty meta items or broken emoji lines
    content = re.sub(r'<span class="meta-item">\s*<\/span>', '', content)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed {filename}")

# Fix all 4 articles
files = [
    'sleep-optimization-20260529.html',
    'ai-drug-discovery-20260529.html', 
    'trt-longevity-20260529.html',
    'apoe4-20260529.html'
]

for file in files:
    if os.path.exists(file):
        fix_article(file)
    else:
        print(f"File not found: {file}")

print("\nAll articles fixed for mobile compatibility!")
