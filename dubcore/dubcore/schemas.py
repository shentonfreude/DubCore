from colander import Schema, SchemaNode, SequenceSchema, MappingSchema
from colander import String, Date, null
from colander import OneOf
import datetime

LANGUAGE_LABELS = ['English', 'Spanish', 'Esperanto']
LANGUAGES = zip(LANGUAGE_LABELS, LANGUAGE_LABELS)

FORMAT_CHOICES = ['text/html', 'text/rst', 'text/plain']
FORMAT_LABELS = ['html', 'rst', 'text']
FORMATS = zip(FORMAT_CHOICES, FORMAT_LABELS)

class Creators(SequenceSchema):
    creator = SchemaNode(String(),
                         title="Creator Name",
                         missing='')

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
    description = SchemaNode(
        String(), missing='',
        description="Short summary returned in search results")
    date = SchemaNode(Date(),  default=datetime.date.today(),
                      description="Created, Modified, ...")
    subject = Subjects(missing=null)
    creator = Creators(missing=null)
    contributor = Contributors(missing=null)
    publisher = SchemaNode(String(),  missing='')
    format = SchemaNode(String(),  missing='',
                        validator=OneOf(FORMAT_CHOICES))
    language = SchemaNode(String(),  missing='', # should use AutoComplete
                          validator=OneOf(LANGUAGE_LABELS))
    type_ = SchemaNode(String(),  name="type", missing='',
                       description="DCMI Type Vocabulary")
    identifier = SchemaNode(String(),  missing='',
                            description="URI")
    source = SchemaNode(String(),  missing='',
                        description="URI")
    relation = SchemaNode(String(),  missing='',
                          description="Is version of, Is part of, ...")
    coverage = SchemaNode(String(),  missing='',
                          description="Spatial and temporal characteristics",)
    rights = SchemaNode(String(),  missing='')

class PageSchema(Schema):
    """Get Page fields and Plone-style uber-common DublinCore fields.
    __name__ like Plone 'id' generated from Title.
    """
    title = DublinCoreSchema.title
    description = DublinCoreSchema.description
    data = SchemaNode(String(), description="Data for the page")


