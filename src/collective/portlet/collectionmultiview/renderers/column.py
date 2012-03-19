from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from collective.portlet.collectionmultiview import BaseRenderer

class ColumnRenderer(BaseRenderer):
    """ display items in a single row table """

    title = 'Column Renderer'
    template = ViewPageTemplateFile('templates/column.pt')

