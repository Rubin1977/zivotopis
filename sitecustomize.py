import sys
import os

""" print("\n=== sitecustomize.py LOADED ===")
for p in sys.path:
    print("  ", p)
print("=== END sys.path ===\n") """

ROOT = os.path.dirname(__file__)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
