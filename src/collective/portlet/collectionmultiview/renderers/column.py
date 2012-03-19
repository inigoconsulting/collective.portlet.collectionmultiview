from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from collective.portlet.collectionmultiview import BaseRenderer

class ColumnRenderer(BaseRenderer):

    title = 'Column Renderer'
    template = ViewPageTemplateFile('templates/column.pt')

