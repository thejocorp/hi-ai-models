#!/usr/bin/env python3
"""Checks catalog.json against catalog.schema.json and refuses anything that looks like a shell command.
Needs: pip install jsonschema. Run: python3 validate.py [catalog.json]"""
import json, re, sys
from jsonschema import Draft202012Validator

path = sys.argv[1] if len(sys.argv) > 1 else "catalog.json"
schema = json.load(open("catalog.schema.json"))
data = json.load(open(path))
bad = [f"{'/'.join(map(str, e.absolute_path))}: {e.message[:200]}" for e in Draft202012Validator(schema).iter_errors(data)]

# the data names models and offers, it never carries commands: no pipes to a shell, no substitution, no install lines
SHELL = re.compile(r"\$\(|`|\|\s*(ba|z)?sh\b|\b(curl|wget|sudo)\s|\brm\s+-")
def walk(v, at=""):
    if isinstance(v, dict):
        for k, x in v.items(): walk(x, f"{at}/{k}")
    elif isinstance(v, list):
        for i, x in enumerate(v): walk(x, f"{at}/{i}")
    elif isinstance(v, str) and SHELL.search(v):
        bad.append(f"{at}: looks like a shell command")
walk(data)

if bad:
    print("catalog.json is not valid:\n" + "\n".join(bad)); sys.exit(1)
print(f"{path} is valid (schema_version {data['schema_version']})")
