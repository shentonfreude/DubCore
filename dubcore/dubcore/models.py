import datetime
from util import canonize
from persistent import Persistent
from repoze.folder import Folder

class Pages(Folder):
    pass

class Page(Persistent):
    """Page has mandatory DublinCore Title, Date.
    We require page.dublincore.title, date to be set here.
    """
    def __init__(self, data, dublincore):
        self.data = data
        if not dublincore['date']:
            raise ValueError("Page.dublincore['date'] is empty")
        if not dublincore['title']:
            raise ValueError("Page.dublincore['title'] is empty")
        self.dublincore = dublincore

def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = Pages()
        zodb_root['app_root'] = app_root

        dublincore = {'title':'Page 1',
                      'date': datetime.date.today(),
                      'description': 'Not much to say',
                      }
        page1 = Page("This is the first page", dublincore)
        __name__ = canonize(page1.dublincore['title'])
        app_root[__name__] = page1

        import transaction
        transaction.commit()
    return zodb_root['app_root']
