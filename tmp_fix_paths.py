import os
import re

base_dir = r"e:\00_YOCHECKIN\Skills"

# Strings to replace
replacements = {
    "Google Antigravity": "00_YOCHECKIN",
    "Google%20Antigravity": "00_YOCHECKIN",
    r"e:/Google Antigravity": "e:/00_YOCHECKIN",
    r"e:\\Google Antigravity": r"e:\\00_YOCHECKIN"
}

# Supported extensions
supported_extensions = {".md", ".py", ".sh", ".txt", ".json", ".html", ".xml", ".txt", ".yaml", ".yml", ".ts", ".js", ".css"}
count = 0
changed_files = []

for root, dirs, files in os.walk(base_dir):
    for name in files:
        if name == "SKILL.md":
            # We already fully updated the main 20 SKILL.md.
            # But wait, there are 11 other SKILL.md files in the old ones!
            # So let's include it.
            pass
            
        ext = os.path.splitext(name)[1].lower()
        if ext in supported_extensions:
            file_path = os.path.join(root, name)
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                continue

            original_content = content
            for old_str, new_str in replacements.items():
                content = content.replace(old_str, new_str)
                
            if content != original_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                changed_files.append(file_path)
                count += 1

print(f"Update complete! Modified {count} files.")
for f in changed_files:
    print(" - " + f)
