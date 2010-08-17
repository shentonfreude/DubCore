import datetime
from webob.exc import HTTPFound
from models import Page
from repoze.bfg.url import model_url
from colander import Schema, SchemaNode, String, Date, MappingSchema
from deform import Form
from deform import widget
from deform import ValidationFailure
#from repoze.bfg.traversal import model_path
import transaction

PROJECT = "Full Of Knobs"

def pages_view(context, request):
    # should use proper way to generate urls (what method?)
    page_urls = [(p, request.application_url + "/" + p) for p in request.context.keys()]
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

class DublinCoreSchema(MappingSchema):
    title = SchemaNode(String(), description="", missing='')
    creator = SchemaNode(String(), description="", missing='')
    subject = SchemaNode(String(), description="", missing='') # TODO should be list
    description = SchemaNode(String(), description="", missing='')
    publisher = SchemaNode(String(), description="", missing='')
    contributor = SchemaNode(String(), description="", missing='')
    date = SchemaNode(Date(), description="", default=datetime.date.today())
    type_ = SchemaNode(String(), description="", missing='')
    format = SchemaNode(String(), description="", missing='')
    identifier = SchemaNode(String(), description="", missing='')
    source = SchemaNode(String(), description="", missing='')
    language = SchemaNode(String(), description="", missing='')
    relation = SchemaNode(String(), description="", missing='')
    coverage = SchemaNode(String(), description="", missing='')
    rights = SchemaNode(String(), description="", missing='')

class PageSchema(Schema):
    name = SchemaNode(String(), description="The Name")
    data = SchemaNode(String(), description="Data for the page")
    dublincore = DublinCoreSchema()

def page_add(context, request):
    add_or_edit = 'Add'
    page_schema = PageSchema()
    page_form = Form(page_schema, buttons=('submit',))
    page_form['data'].widget = widget.TextAreaWidget(rows=10, cols=60)
    if 'submit' in request.params: # or method==POST
        controls = request.POST.items()
        import pdb; pdb.set_trace()
        try:
            appstruct = page_form.validate(controls)
        except ValidationFailure, e:
            return {'project': PROJECT,
                    'form': e.render(),
                    'add_or_edit': add_or_edit}
        page = Page(appstruct['data'], dublincore=appstruct['dublincore'])
        context[appstruct['name']] = page
        #Needed?? transaction.commit()
        return HTTPFound(location=model_url(page, request))
    return {'project': PROJECT,
            'form': page_form.render(),
            'add_or_edit': add_or_edit,
            }

def page_edit(context, request):
    add_or_edit = 'Edit'
    page_schema = PageSchema()
    page_form = Form(page_schema, buttons=('submit',))
    page_form['name'].widget = widget.HiddenWidget() # don't let them edit the name (yet)
    page_form['data'].widget = widget.TextAreaWidget(rows=10, cols=60)
    if 'submit' in request.params: # or method==POST
        controls = request.POST.items()
        try:
            appstruct = page_form.validate(controls)
        except ValidationFailure, e:
            return {'project': PROJECT,
                    'form': e.render(),
                    'add_or_edit': add_or_edit}
        context.data = appstruct['data']
        context.dublincore = appstruct['dublincore']
        return HTTPFound(location=model_url(context, request))
    appstruct = context.__dict__
    return {'project': PROJECT,
            'form': page_form.render(appstruct),
            'add_or_edit': add_or_edit,
            }

def page_edit_dc(context, request):
    """Edit the DublinCore attributes of a Page."""
    dc_schema = DublinCoreSchema()
    dc_form = Form(dc_schema, buttons=('submit',))
    if 'submit' in request.params: # or method==POST
        controls = request.POST.items()
        try:
            appstruct = dc_form.validate(controls)
        except ValidationFailure, e:
            return {'project': PROJECT,
                    'form': e.render(),
                    }
        context.dublincore = appstruct
        return HTTPFound(location=model_url(context, request))
    appstruct = context.__dict__
    return {'project': PROJECT,
            'form': dc_form.render(appstruct),
            }
