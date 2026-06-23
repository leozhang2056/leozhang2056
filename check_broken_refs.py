#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check for broken image references in all project READMEs."""

import re
from pathlib import Path

projects_dir = Path(r"E:\Coding\leozhang2056\projects")

broken_refs = []
total_refs = 0

for project in sorted(projects_dir.iterdir()):
    if not project.is_dir() or project.name in ("nul", ".venv"):
        continue
    
    readme_file = project / "README.md"
    if not readme_file.exists():
        continue
    
    readme_content = readme_file.read_text(encoding='utf-8')
    
    # Find all image references: src="./images/xxx" or src="images/xxx" or ![xxx](images/xxx)
    # Pattern 1: HTML img tags: src="./images/filename" or src="images/filename"
    html_refs = re.findall(r'src=["\'](?:\./)?images/([^"\']+)["\']', readme_content)
    
    # Pattern 2: Markdown images: ![alt](images/filename) or ![alt](./images/filename)
    md_refs = re.findall(r'!\[.*?\]\((?:\./)?images/([^)]+)\)', readme_content)
    
    all_refs = set(html_refs + md_refs)
    
    images_dir = project / "images"
    
    for ref in sorted(all_refs):
        total_refs += 1
        img_path = images_dir / ref
        
        if not img_path.exists():
            broken_refs.append((project.name, ref))

print("=" * 80)
print("BROKEN IMAGE REFERENCES CHECK")
print("=" * 80)

if broken_refs:
    print(f"\nFound {len(broken_refs)} broken references:\n")
    for pname, ref in broken_refs:
        print(f"  [!!] {pname}/README.md -> images/{ref}")
        # Check if similar file exists
        images_dir = projects_dir / pname / "images"
        if images_dir.exists():
            # Find similar files
            similar = [f.name for f in images_dir.iterdir() 
                      if f.suffix.lower() == Path(ref).suffix.lower()
                      and f.name.lower().startswith(ref[:5].lower())]
            if similar:
                print(f"       Similar files: {', '.join(similar[:5])}")
else:
    print(f"\nAll {total_refs} image references are valid!")

print(f"\n{'=' * 80}")
print(f"Total references checked: {total_refs}")
print(f"Broken references: {len(broken_refs)}")
print("=" * 80)
