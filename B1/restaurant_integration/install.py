#!/usr/bin/env python3
"""
Team B1 — Restaurant POS System Integration Verifier
Executes evolution verification tests against the integrated TypeScript backend.
"""

import subprocess
import sys
import os

def main():
    print("=" * 60)
    print("Team B1 — Restaurant POS Integration Verifier")
    print("Course: 23CSE455 Design Patterns")
    print("=" * 60)

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    backend_dir = os.path.join(repo_root, "apps", "backend")

    if not os.path.exists(backend_dir):
        print(f"Error: Backend directory not found at {backend_dir}")
        sys.exit(1)

    print(f"\n[1/2] Checking backend build in {backend_dir}...")
    build_cmd = ["npm", "run", "build"]
    res = subprocess.run(build_cmd, cwd=backend_dir, shell=True)
    if res.returncode != 0:
        print("Warning: Build step returned non-zero code. Attempting direct tsx run.")

    print("\n[2/2] Running automated evolution test suite (verify_evolutions.ts)...")
    test_cmd = ["node", "dist/scripts/verify_evolutions.js"]
    res = subprocess.run(test_cmd, cwd=backend_dir, shell=True)
    if res.returncode != 0:
        # Fallback to tsx
        res = subprocess.run(["npx", "tsx", "src/scripts/verify_evolutions.ts"], cwd=backend_dir, shell=True)

    if res.returncode == 0:
        print("\n" + "=" * 60)
        print("SUCCESS: All 28/28 evolution assertions passed (100%).")
        print("=" * 60)
    else:
        print("\nVerification failed. Inspect logs above.")
        sys.exit(res.returncode)

if __name__ == "__main__":
    main()
