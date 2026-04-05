#!/usr/bin/env python3
"""Fix Unicode encoding issues in test файл"""
import sys
import os

# Fix file path
file_path = os.path.join(os.path.dirname(__file__), "tests", "test_summary.py")

print(f"[*] Reading file: {file_path}")

# Read the file with UTF-8
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"[OK] File read successfully ({len(content)} characters)")
except Exception as e:
    print(f"[ERROR] Failed to read: {e}")
    sys.exit(1)

# Count and replace Unicode chars
replacements = {
    '✓': '[OK]',
    '✗': '[FAIL]',
    '⚠️': '[WARN]',
    '❌': '[ERROR]',
    '·': '.',
    '•': '*',  # bullet point to asterisk
}

total_replaced = 0
for old, new in replacements.items():
    count = content.count(old)
    if count > 0:
        print(f"[*] Replacing '{old}' → '{new}': {count} occurrences")
        content = content.replace(old, new)
        total_replaced += count

print(f"[OK] Total replacements: {total_replaced}")

# Write back with ASCII-safe encoding
try:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] File written successfully")
except Exception as e:
    print(f"[ERROR] Failed to write: {e}")
    sys.exit(1)

print(f"[OK] Unicode encoding fix complete!")
