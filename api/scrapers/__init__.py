import os
import importlib

# Import all scraper_*.py files automatically
for filename in os.listdir(os.path.dirname(__file__)):
    if filename.startswith("scraper_") and filename.endswith(".py") and filename != "scraper_factory.py" and filename != "scraper_registry.py":
        importlib.import_module(f"{__name__}.{filename[:-3]}")
