import os

base_dir = r"e:\00_YOCHECKIN\Skills"
report = []

for skill_dir in os.listdir(base_dir):
    full_path = os.path.join(base_dir, skill_dir)
    if os.path.isdir(full_path):
        refs = os.path.join(full_path, "references")
        scripts = os.path.join(full_path, "scripts")
        
        ref_files = []
        if os.path.isdir(refs):
            ref_files = os.listdir(refs)
            
        script_files = []
        if os.path.isdir(scripts):
            script_files = os.listdir(scripts)
            
        other_files = [f for f in os.listdir(full_path) if f != "SKILL.md" and f != "references" and f != "scripts" and os.path.isfile(os.path.join(full_path, f))]
        
        report.append(f"{skill_dir}: {len(ref_files)} ref files, {len(script_files)} script files, {len(other_files)} others")

with open(r"e:\00_YOCHECKIN\tmp_report.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print("Analysis complete!")
