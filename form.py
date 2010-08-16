from paste.httpserver import serve
from repoze.bfg.configuration import Configurator

from colander import MappingSchema
from colander import SequenceSchema
from colander import SchemaNode
from colander import String
from colander import Boolean
from colander import Integer
from colander import Length
from colander import OneOf

from deform import ValidationFailure
from deform import Form
from deform import widget

class DateSchema(MappingSchema):
    year = SchemaNode(Integer())
    month = SchemaNode(Integer()) # validator 1..12
    day = SchemaNode(Integer()) # validator.. 1..31
    # validator ensure Days approp to Month

class DublinCoreSchema(MappingSchema):
    title = SchemaNode(String(), description="")
    creator = SchemaNode(String(), description="")
    subject = SchemaNode(String(), description="")
    description = SchemaNode(String(), description="")
    publisher = SchemaNode(String(), description="")
    contributor = SchemaNode(String(), description="")
    date = SchemaNode(DateSchema(), description="") # Correct Use?
    type_ = SchemaNode(String(), description="")
    format = SchemaNode(String(), description="")
    identifier = SchemaNode(String(), description="")
    source = SchemaNode(String(), description="")
    language = SchemaNode(String(), description="")
    relation = SchemaNode(String(), description="")
    coverage = SchemaNode(String(), description="")
    rights = SchemaNode(String(), description="")


def form_view(request):
    dc_schema = DublinCoreSchema()
    myform = Form(dc_schema, buttons=('submit',))
    myform['title'].widget = widget.TextInputWidget(size=60)
    
    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            myform.validate(controls)
        except ValidationFailure, e:
            return {'form': e.render()}
        return {'form': 'OK'}
    return {'form': myform.render()}

if __name__ == '__main__':
    settings = dict(reload_template=True)
    config = Configurator(settings=settings)
    config.begin()
    config.add_static_view('static', 'deform:static')
    config.end()
    app = config.make_wsgi_app()
    serve(app)

