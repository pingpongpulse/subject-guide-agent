# Fix Unicode encoding issues in test files
import os

file_path = "tests/test_summary.py"

# Read file with UTF-8 encoding
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Unicode characters with ASCII-safe alternatives
content = content.replace('✓', '[OK]')
content = content.replace('✗', '[FAIL]')
content = content.replace('⚠️', '[WARN]')
content = content.replace('❌', '[ERROR]')
content = content.replace('·', '.')

# Write back with UTF-8
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"[OK] Fixed Unicode encoding issues in {file_path}")
