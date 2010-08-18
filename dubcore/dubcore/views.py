import datetime
from util import canonize
from webob.exc import HTTPFound
from models import Page
from repoze.bfg.url import model_url
from colander import Schema, SchemaNode, String, Date
from colander import MappingSchema, SequenceSchema
from colander import OneOf
from deform import Form
from deform import widget
from deform import ValidationFailure
from repoze.bfg.settings import get_settings

PROJECT = get_settings()['project']
LANGUAGE_LABELS = ['English', 'Spanish', 'Esperanto']
LANGUAGES = zip(LANGUAGE_LABELS, LANGUAGE_LABELS)
FORMAT_LABELS = ['html', 'rst', 'text']
FORMAT_CHOICES = ['text/html', 'text/rst', 'text/plain']
FORMATS = zip(FORMAT_CHOICES, FORMAT_LABELS)

class Creators(SequenceSchema):
    creator = SchemaNode(String(), missing='', title="Creator Name")

class Subjects(SequenceSchema):
    subject = SchemaNode(String(),
                         title="Subject Keyword",
                         description="Keyword or Tag",
                         missing='')

class Contributors(SequenceSchema):
    contributor_name = SchemaNode(String(),
                                  title="Contributor Name",
                                  missing='')

class DublinCoreSchema(MappingSchema):
    title = SchemaNode(String())
    creator = Creators()
    subject = Subjects()
    description = SchemaNode(
        String(), missing='',
        description="Short summary returned in search results")
    publisher = SchemaNode(String(),  missing='')
    contributor = Contributors()
    date = SchemaNode(Date(),  default=datetime.date.today())
    type_ = SchemaNode(String(),  name="type", missing='') # WTF is this?
    format = SchemaNode(String(),  missing='',
                        validator=OneOf(FORMAT_CHOICES))
    identifier = SchemaNode(String(),  missing='')
    source = SchemaNode(String(),  missing='')
    language = SchemaNode(String(),  missing='', # should use AutoComplete
                          validator=OneOf(LANGUAGE_LABELS))
    relation = SchemaNode(String(),  missing='')
    coverage = SchemaNode(String(),  missing='')
    rights = SchemaNode(String(),  missing='')

class PageSchema(Schema):
    """Get Page fields and Plone-style uber-common DublinCore fields.
    __name__ like Plone 'id' generated from Title.
    """
    title = DublinCoreSchema.title
    description = DublinCoreSchema.description
    data = SchemaNode(String(), description="Data for the page")


def pages_view(context, request):
    page_urls = [(context[p].dublincore['title'],
                  model_url(context, request, p)) for p in request.context.keys()]
    return {'project': PROJECT,
            'page_urls': page_urls,
            'page_add_url': model_url(context, request, "@@page_add")
            }

def page_view(context, request):
    dc_schema = DublinCoreSchema()
    dc_form = Form(dc_schema)
    return {'project': PROJECT,
            'page': context,
            'dc_form': dc_form.render(context.dublincore, readonly=True),
            'page_edit_url': model_url(context, request, "@@page_edit"),
            'page_edit_dc_url': model_url(context, request, "@@page_edit_dc")
            }

def page_add(context, request):
    add_or_edit = 'Add'
    schema = PageSchema()
    form = Form(schema, buttons=('submit',))
    form['data'].widget = widget.RichTextWidget(width=390, theme="advanced")
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
    form['data'].widget = widget.RichTextWidget(theme="advanced")
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
    form['rights'].widget = widget.RichTextWidget()
    form['language'].widget = widget.SelectWidget(values=LANGUAGES)
    form['format'].widget = widget.SelectWidget(values=FORMATS)
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
