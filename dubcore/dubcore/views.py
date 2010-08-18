import datetime
from util import canonize
from webob.exc import HTTPFound
from models import Page
from repoze.bfg.url import model_url
from colander import Schema, SchemaNode, String, Date, MappingSchema
from deform import Form
from deform import widget
from deform import ValidationFailure
#from repoze.bfg.traversal import model_path
import transaction

# TODO: use the new wysiwyg text area editor.

PROJECT = "Full Of Knobs"

def pages_view(context, request):
    page_urls = [(context[p].dublincore['title'],
                  model_url(context, request, p)) for p in request.context.keys()]
    return {'project': PROJECT,
            'page_urls': page_urls,
            'page_add_url': model_url(context, request, "@@page_add")
            }

def page_view(context, request):
    return {'project': PROJECT,
            'page': context,
            'page_edit_url': model_url(context, request, "@@page_edit"),
            'page_edit_dc_url': model_url(context, request, "@@page_edit_dc")
            }

# TODO: make list-ish things sequences of Schemas
class DublinCoreSchema(MappingSchema):
    title = SchemaNode(String())
    creator = SchemaNode(String(), description="Creators", missing='') # TODO list
    subject = SchemaNode(String(), description="Keywords/Tags", missing='') # TODO should be list
    description = SchemaNode(String(), description="Short summary returned in search results", missing='')
    publisher = SchemaNode(String(),  missing='')
    contributor = SchemaNode(String(),  missing='') # TODO list
    date = SchemaNode(Date(),  default=datetime.date.today())
    type_ = SchemaNode(String(),  missing='') # WTF is this?
    format = SchemaNode(String(),  missing='') # TODO picklist: html, rst, ...
    identifier = SchemaNode(String(),  missing='')
    source = SchemaNode(String(),  missing='')
    language = SchemaNode(String(),  missing='')
    relation = SchemaNode(String(),  missing='')
    coverage = SchemaNode(String(),  missing='')
    rights = SchemaNode(String(),  missing='') # TODO textarea

class PageSchema(Schema):
    """Get Page fields and Plone-style uber-common DublinCore fields.
    __name__ like Plone 'id' generated from Title.
    """
    title = DublinCoreSchema.title
    description = DublinCoreSchema.description
    data = SchemaNode(String(), description="Data for the page")

def page_add(context, request):
    add_or_edit = 'Add'
    schema = PageSchema()
    form = Form(schema, buttons=('submit',))
    form['data'].widget = widget.TextAreaWidget(rows=10, cols=60)
    if 'submit' in request.params: # or method==POST
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except ValidationFailure, e:
            return {'project': PROJECT,
                    'form': e.render(),
                    'add_or_edit': add_or_edit}
        # Is there a way to get this -- the date especialy -- from the schema?
        dublincore = {'title': appstruct['title'],
                      'description': appstruct['description'],
                      'date': datetime.date.today(),
                      }
        page = Page(appstruct['data'], dublincore=dublincore)
        __name__ = canonize(appstruct['title'])
        # TODO: if title changed remove old __name__
        context[__name__] = page
        return HTTPFound(location=model_url(page, request))
    return {'project': PROJECT,
            'form': form.render(),
            'add_or_edit': add_or_edit,
            }

# TODO: change __name__ if Title changed
def page_edit(context, request):
    add_or_edit = 'Edit'
    schema = PageSchema()
    form = Form(schema, buttons=('submit',))
    form['data'].widget = widget.TextAreaWidget(rows=10, cols=60)
    if 'submit' in request.params: # or method==POST
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except ValidationFailure, e:
            return {'project': PROJECT,
                    'form': e.render(),
                    'add_or_edit': add_or_edit}
        # TODO: if title changed remove old __name__
        context.data = appstruct['data']
        context.dublincore['title'] = appstruct['title']
        context.dublincore['description'] = appstruct['description']
        return HTTPFound(location=model_url(context, request))
    # Is there an easier way to do this?
    #appstruct = context.__dict__
    appstruct = {'data': context.data,
                 'title': context.dublincore['title'],
                 'description': context.dublincore['description'],
                 }
    return {'project': PROJECT,
            'form': form.render(appstruct),
            'add_or_edit': add_or_edit,
            }

# TODO: change __name__ if Title changed
def page_edit_dc(context, request):
    """Edit the DublinCore attributes of a Page."""
    schema = DublinCoreSchema()
    form = Form(schema, buttons=('submit',))
    if 'submit' in request.params: # or method==POST
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except ValidationFailure, e:
            return {'project': PROJECT,
                    'form': e.render(),
                    }
        context.dublincore = appstruct
        return HTTPFound(location=model_url(context, request))
    appstruct = context.dublincore
    return {'project': PROJECT,
            'form': form.render(appstruct),
            }
