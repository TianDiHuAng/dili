# -*- coding: utf-8 -*-
"""tools/check_links.py — 站内链接完整性核验（直到 0 断链）。"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
PAT = re.compile(r'(?:href|src)="([^"#][^"]*)"')

def main():
    broken = []
    checked = 0
    for dirpath, _, files in os.walk(SITE):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(dirpath, fn)
            with open(p, encoding="utf-8") as f:
                text = f.read()
            for m in PAT.finditer(text):
                href = m.group(1).split("#")[0].split("?")[0]
                if not href or href.startswith(("http://", "https://", "mailto:", "javascript:")):
                    continue
                checked += 1
                target = os.path.normpath(os.path.join(dirpath, href))
                if not os.path.exists(target):
                    broken.append(f"{os.path.relpath(p, SITE)} -> {href}")
    print(f"检查内部链接 {checked} 条")
    if broken:
        print(f"BROKEN={len(broken)}")
        for b in broken[:100]:
            print("  X", b)
        sys.exit(1)
    print("BROKEN=0 LINKS_PASS")

if __name__ == "__main__":
    main()
