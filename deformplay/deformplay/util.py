import unicodedata
import re

def canonize(title):
    """make url ready string/id from a title"""
    title = unicode(title)
    url_safer = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore')
    url_safe = unicode(re.sub('[^\w\s-]', '', url_safer).strip().lower())
    return re.sub('[-\s]+', '-', url_safe)

