from webob.exc import HTTPFound
from models import Page
from repoze.bfg.url import model_url
import colander
from deform import Form
#from deform import widget
from deform import ValidationFailure
#from repoze.bfg.traversal import model_path
import transaction

def pages_view(context, request):
    page_urls = [(p, request.application_url + "/" + p) for p in request.context.keys()]
    return {'project': 'PAGES',
            'page_urls': page_urls,
            'page_add_url': model_url(context, request, "@@page_add")
            }

def page_view(context, request):
    return {'project': 'PAGE',
            'page': context,
            'page_edit_url': model_url(context, request, "@@page_edit"),
            }

class DCSchema(colander.Schema):
    data = colander.SchemaNode(colander.String(), description="Data for the page")
    date = colander.SchemaNode(colander.Date(), description="The Date")


def page_add(context, request):
    add_or_edit = 'Add'
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
            return {'form': e.render(),
                    'add_or_edit': add_or_edit}
        page = Page(appstruct['data'], appstruct['date'])
        context[appstruct['name']] = page
        transaction.commit()
        return HTTPFound(location=model_url(page, request))

    return {'form': dcform.render(),
            'add_or_edit': add_or_edit,
            }

def page_edit(context, request):
    print "PAGE EDIT"
    add_or_edit = 'Edit'
    dcschema = DCSchema()
    dcform = Form(dcschema, buttons=('submit',))
    if 'submit' in request.params: # or method==POST
        print "FORM SUBMITTED"
        controls = request.POST.items()
        try:
            appstruct = dcform.validate(controls)
            print "PAGE ADD appstruct=%s" % appstruct
        except ValidationFailure, e:
            return {'form': e.render(),
                    'add_or_edit': add_or_edit}
        context['date'] = appstruct['date']
        context['data'] = appstruct['data']
        return HTTPFound(location=model_url(context, request))
    # TODO: populate form with context
    return {'form': dcform.render(),
            'add_or_edit': add_or_edit,
            }
