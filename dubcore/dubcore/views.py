# TODO: change __name__ if Title changes in Page or DublinCore (or not?)

import datetime
from util import canonize
from webob.exc import HTTPFound
from models import Page
from repoze.bfg.url import model_url
from repoze.bfg.settings import get_settings
from deform import Form
from deform import widget
from deform import ValidationFailure
from schemas import DublinCoreSchema, PageSchema
from schemas import LANGUAGES, FORMATS

PROJECT = get_settings()['project']

def pages_view(context, request):
    page_urls = [(context[p].dublincore['title'],
                  model_url(context, request, p))
                 for p in request.context.keys()]
    return {'project': PROJECT,
            'page_urls': page_urls,
            'page_add_url': model_url(context, request, "@@page_add")
            }

def page_view(context, request):
    dc_schema = DublinCoreSchema()
    dc_form = Form(dc_schema)
    dc_form['subject'].widget.category = None # HACK: display sequence label
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
    if 'submit' in request.params:
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
        context[__name__] = page
        return HTTPFound(location=model_url(page, request))
    return {'project': PROJECT,
            'form': form.render(),
            'add_or_edit': add_or_edit,
            }

def page_edit(context, request):
    add_or_edit = 'Edit'
    schema = PageSchema()
    form = Form(schema, buttons=('submit',))
    form['data'].widget = widget.RichTextWidget(theme="advanced")
    if 'submit' in request.params:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except ValidationFailure, e:
            return {'project': PROJECT,
                    'form': e.render(),
                    'add_or_edit': add_or_edit}
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

def page_edit_dc(context, request):
    """Edit the DublinCore attributes of a Page."""
    schema = DublinCoreSchema()
    form = Form(schema, buttons=('submit',))
    form['description'].widget = widget.TextAreaWidget(rows=10, cols=40)
    form['subject'].widget.category = None     # HACK: display sequence label
    form['creator'].widget.category = None     # HACK: display sequence label
    form['contributor'].widget.category = None # HACK: display sequence label
    form['rights'].widget = widget.TextAreaWidget(rows=10, cols=40)
    form['language'].widget = widget.SelectWidget(values=LANGUAGES)
    form['format'].widget = widget.SelectWidget(values=FORMATS)
    if 'submit' in request.params:
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
