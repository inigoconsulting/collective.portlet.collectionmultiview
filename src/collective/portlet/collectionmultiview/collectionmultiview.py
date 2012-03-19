from zope.interface import implements,alsoProvides
from zope.component import adapts,getAdapter,getAdapters

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.portlet.collection import collection

from zope import schema
from zope.formlib import form
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from collective.portlet.collectionmultiview.i18n import messageFactory as _
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from interfaces import ICollectionMultiViewBaseRenderer, ICollectionMultiViewRenderer
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from collective.portlet.collectionmultiview.widget import RendererSelectWidget


class ICollectionMultiView(IPortletDataProvider):

    header = schema.TextLine(
        title=_(u"Portlet header"),
        description=_(u"Title of the rendered portlet"),
        required=True)

    target_collection = schema.Choice(
        title=_(u"Target collection"),
        description=_(u"Find the collection which provides the items to list"),
        required=True,
        source=SearchableTextSourceBinder(
            {'portal_type': 'Topic'},
            default_query='path:'))

    limit = schema.Int(
        title=_(u"Limit"),
        description=_(u"Specify the maximum number of items to show in the "
                      u"portlet. Leave this blank to show all items."),
        required=False)

    renderer = schema.Choice(title=_(u'Renderer'),
                         description=_(u"The name of the Renderer for this portlet."),
                         default='default',
                         required=True,
                         vocabulary='collective.portlet.collectionmultiview.RendererVocabulary')


class Assignment(base.Assignment):

    implements(ICollectionMultiView)

    header = u""
    target_collection = None
    limit = None

    def __init__(self, header=u"", target_collection=None, limit=None,
                 renderer='default'):
        self.header = header
        self.target_collection = target_collection
        self.limit = limit
        self.renderer = renderer

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.header


class Renderer(collection.Renderer):
    implements(ICollectionMultiViewBaseRenderer)

    @property
    def render(self):
        """
            Find the renderer object of the selected renderer, and let it
            masquerade as the actual portlet renderer
        """
        renderer = getattr(self.data,'renderer',None)
        if renderer is None:
           self.data.renderer = 'default'
           renderer = 'default'
        return getAdapter(self, ICollectionMultiViewRenderer, renderer).render


def get_extended_schema(request, renderer=u'default'):
    """
        Find the schema that should be displayed
    """
    if request.get('form.renderer'):
        # during refresh when changing renderer
        renderer = request.get('form.renderer')

    adapter = getAdapter(None, ICollectionMultiViewRenderer, renderer)
    schema = getattr(adapter, 'schema', None)
    iface = ICollectionMultiView
    if schema is not None:
        class IExtendedSchema(iface, schema): pass
        iface = IExtendedSchema
    return iface
        
class AddForm(base.AddForm):

    @property
    def form_fields(self):
        schema = get_extended_schema(self.request)
        fields = form.Fields(schema)
        fields['target_collection'].custom_widget = UberSelectionWidget
        fields['renderer'].custom_widget = RendererSelectWidget
        return fields

    label = _(u'Add CollectionMultiView portlet')
    description = _(u"This portlet display a listing of items from a" + 
                        " Collection, using custom views")

    def create(self, data):
        return Assignment(**data)



class ExtendedDataAdapter(object):
    """ 
        hack to lie to form.applyChanges that this object have
        all attributes
    """

    def __init__(self, context):
        self.context = context

    def __setattr__(self, key, value):
        if key != 'context':
            setattr(self.context, key, value)
        else:
            super(ExtendedDataAdapter, self).__setattr__(key, value)

    def __getattr__(self, key):
        if key != 'context':
            return getattr(self.context, key, None)
        else:
            return super(ExtendedDataAdapter, self).__getattr__(key)

class EditForm(base.EditForm):

    @property
    def form_fields(self):
        schema = get_extended_schema(self.request, self.context.renderer)
        fields = form.Fields(schema)
        fields['target_collection'].custom_widget = UberSelectionWidget
        fields['renderer'].custom_widget = RendererSelectWidget
        if getattr(self, 'adapters', None) is not None:
            self.adapters[schema] = ExtendedDataAdapter(self.context)
        return fields

    label = _(u'Edit CollectionMultiView portlet')
    description = _(u"This portlet display a listing of items from a" +
                        " Collection, using custom views")
