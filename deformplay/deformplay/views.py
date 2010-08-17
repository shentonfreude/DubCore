from webob.exc import HTTPFound
from models import Page
from repoze.bfg.url import model_url
import colander
from deform import Form
from deform import widget
from deform import ValidationFailure
import transaction

def pages_view(request):
    page_urls = [(p, request.application_url + "/" + p) for p in request.context.keys()]
    return {'project': 'PAGES',
            'page_urls': page_urls,
            }

def page_view(request):
    return {'project': 'PAGE',
            'page': request.context,
            }

class DCSchema(colander.Schema):
    data = colander.SchemaNode(colander.String(), description="Data for the page")
    date = colander.SchemaNode(colander.Date(), description="The Date")

from repoze.bfg.traversal import model_path
def page_add(context, request):
    # The context should be Pages, but is a Page
    print "PAGE ADD context=%s" % context
    print "PAGE ADD model_path=%s" % model_path(context)
    dcschema = DCSchema()
    # TODO can I add the name before the other fields?
    dcschema.add(colander.SchemaNode(colander.String(), name='name', description="The Name"))
    dcform = Form(dcschema, buttons=('submit',))
    if 'submit' in request.params: # or method==POST
        controls = request.POST.items()
        try:
            appstruct = dcform.validate(controls)
            print "PAGE ADD appstruct=%s" % appstruct
        except ValidationFailure, e:
            return {'form': e.render()}
        page = Page(appstruct['data'], appstruct['date'])
        page.__name__ = appstruct['name']
        page.__parent__ = context
        context[page.__name__] = page
        transaction.commit()
        return HTTPFound(location=model_url(page, request))

    return {'form': dcform.render()}

def page_edit(context, request):
    print "PAGE EDIT"
    if 'submit' in request.params: # or method==POST
        print "FORM SUBMITTED"
        context.data = request.params['data']
        context.date = request.params['date']
        # TODO Validate? or colander does it for me
        page = Page(data, date)
        page.__name__ = name
        page.__parent__ = context
        return HTTPFound(location=model_url(page, request))
    # TODO: populate form with context
    dcschema = DCSchema()
    dcform = Form(dcschema, buttons=('submit',))
    return {'form': dcform.render(),
            }
