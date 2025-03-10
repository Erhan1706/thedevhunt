# A global dictionary to hold name -> class mappings
registry = {}

def register_scraper(name):
    def decorator(cls):
        registry[name] = cls
        return cls
    return decorator