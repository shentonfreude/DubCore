import datetime
from persistent import Persistent
from persistent.mapping import PersistentMapping

class Pages(PersistentMapping): # repoze.folder

    __name__ = None
    __parent__ = None

class Page(Persistent):
    def __init__(self, data, date=None):
        self.data = data
        if not date:
            self.date=datetime.date.today()
        else:
            self.date = date

def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = Pages()
        zodb_root['app_root'] = app_root

        page1 = Page("This is a page")
        app_root['page1'] = page1
        page1.__name__ = "page1"
        page1.__parent__ = app_root

        import transaction
        transaction.commit()
    return zodb_root['app_root']
