import trafilatura

# parse page content from url use trafilatura library
def parse_page(text: str):
    if text:
        text = trafilatura.extract(text)
        return text
    else:
        return None