#!/usr/bin/env python3
"""Apply the A5 Laravel overlay to a checkout of the inspected upstream commit.
Idempotent, never alters upstream Git remote. Use a clean checkout.
"""
from pathlib import Path
import argparse
import shutil
import sys
import re

p=argparse.ArgumentParser()
p.add_argument("upstream",type=Path)
a=p.parse_args()
root=a.upstream.resolve()
src=Path(__file__).resolve().parent
if not (root/"artisan").exists() or not (root/"bootstrap"/"providers.php").exists():
    sys.exit("Expected a Laravel 12 project with artisan and bootstrap/providers.php")
for rel in ["app/Services/CaseStudy/Integrations.php",
            "app/Http/Controllers/CaseStudy/IntegrationController.php",
            "app/Providers/CaseStudyIntegrationProvider.php",
            "config/case_study.php","routes/case_study.php",
            "tests/Feature/CaseStudyIntegrationsTest.php"]:
    dst=root/rel
    dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(src/rel,dst)
providers=root/"bootstrap/providers.php"
text=providers.read_text()
entry="App\\Providers\\CaseStudyIntegrationProvider::class,"
if entry not in text:
    if not re.search(r"\];\s*$",text):
        sys.exit("Unsupported bootstrap/providers.php format")
    text=re.sub(r"\];\s*$",lambda match: "    "+entry+"\n];\n",text)
    providers.write_text(text)
routes=root/"routes/web.php"
text=routes.read_text()
entry="require __DIR__.'/case_study.php';"
if entry not in text:
    routes.write_text(text.rstrip()+"\n\n"+entry+"\n")
print("Applied A5 integration overlay. Review git diff before deployment.")
