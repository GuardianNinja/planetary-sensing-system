#!/usr/bin/env python
"""scripts/dev_run.py - Development runner for SLOS-Kernel.

Starts the FastAPI server with hot-reload.
Usage: python scripts/dev_run.py
"""

import sys
import os

# Add src to path so imports work correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import uvicorn

if __name__ == "__main__":
    print()
    print("="*60)
    print("🛡️  SLOS-KERNEL: Governed Digital Civilization")
    print("="*60)
    print()
    print("Starting development server...")
    print("API Docs: http://localhost:8000/docs")
    print("Ingress Gateway: POST http://localhost:8000/v1/intent")
    print()

    uvicorn.run(
        "src.runtime.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
