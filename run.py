#!/usr/bin/env python
"""
Entry point for GenIA E2E Test Generator.
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.main import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
