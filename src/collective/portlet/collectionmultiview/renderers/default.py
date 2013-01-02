from collective.portlet.collectionmultiview import BaseRenderer
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from zope.interface import Interface
from zope import schema
from collective.portlet.collectionmultiview.i18n import messageFactory as _

class IDefaultSchema(Interface):
    show_more = schema.Bool(
        title=_(u"Show more... link"),
        description=_(u"If enabled, a more... link will appear in the footer "
                      u"of the portlet, linking to the underlying "
                      u"Collection."),
        default=True)

    show_dates = schema.Bool(
        title=_(u"Show dates"),
        description=_(u"If enabled, effective dates will be shown underneath "
                      u"the items listed."),
        default=False)


class DefaultRenderer(BaseRenderer):
    """ the default renderer from plone.portlet.collection """

    title = 'Default Renderer'
    schema = IDefaultSchema
    template = ViewPageTemplateFile('templates/default.pt')
