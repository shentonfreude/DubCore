
from persistent import Persistent
from repoze.folder import Folder

class Pages(Folder):
    pass

class Page(Persistent):
    def __init__(self, data, date=None, dublincore=None):
        self.data = data
        if dublincore == None:
            self.dublincore = {}
        else:
            self.dublincore = dublincore

def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = Pages()
        zodb_root['app_root'] = app_root

        page1 = Page("This is a page")
        app_root['page1'] = page1

        import transaction
        transaction.commit()
    return zodb_root['app_root']
