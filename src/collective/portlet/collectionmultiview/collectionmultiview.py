from zope.interface import implements,alsoProvides
from zope.component import adapts,getAdapter,getAdapters

from plone.app.portlets.portlets import base
from plone.portlet.collection import collection

from zope import schema
from zope.formlib import form
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from collective.portlet.collectionmultiview import CollectionMultiViewMessageFactory as _
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from interfaces import ICollectionMultiViewBaseRenderer,ICollectionMultiViewRenderer
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary,SimpleTerm

# FIXME: hack to query for available adapters
# no idea on what the better way to do this
class FakeRenderer(object):
    implements(ICollectionMultiViewBaseRenderer)
    def __init__(self):
        for attr in ['request', 'context', 'data', 'results',
                     'collection_url', 'collection']:
            setattr(self, attr, None)

def RendererVocabulary(context):
    fake = FakeRenderer()
    adapters = getAdapters((fake, ),ICollectionMultiViewRenderer)
    terms = []
    for name, adapted in adapters:
        title = getattr(adapted, '__name__', name)
        terms.append(SimpleVocabulary.createTerm(title))
    return SimpleVocabulary(terms)

alsoProvides(RendererVocabulary, IVocabularyFactory)


class ICollectionMultiView(collection.ICollectionPortlet):

    renderer = schema.Choice(title=_(u'Renderer'),
                         description=_(u"The name of the Renderer for this portlet."),
                         default='default',
                         required=True,
                         vocabulary='collective.portlet.collectionmultiview.RendererVocabulary')


class Assignment(collection.Assignment):

    implements(ICollectionMultiView)

    def __init__(self, header=u"", target_collection=None, limit=None,
                 random=False, show_more=True, show_dates=False, 
                 renderer='default'):
        super(Assignment,self).__init__(header, target_collection, limit, 
                                        random, show_more, show_dates)
        self.renderer = renderer


class Renderer(collection.Renderer):
    implements(ICollectionMultiViewBaseRenderer)

    @property
    def render(self):
        renderer = getattr(self.data,'renderer',None)
        if renderer is None:
           self.data.renderer = 'default'
           renderer = 'default'
        return getAdapter(self, ICollectionMultiViewRenderer, renderer).render


class AddForm(collection.AddForm):

    form_fields = form.Fields(ICollectionMultiView)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
    # hide these fields from collectionportlet, we dont need these here
    form_fields = form_fields.omit('random', 'show_more', 'show_dates')

    label = _(u'Add CollectionMultiView portlet')
    description = _(u"This portlet display a listing of items from a" + 
                        " Collection, using custom views")

    def create(self, data):
        return Assignment(**data)


class EditForm(collection.EditForm):

    form_fields = form.Fields(ICollectionMultiView)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
    # hide these fields from collectionportlet, we dont need these here
    form_fields = form_fields.omit('random', 'show_more', 'show_dates')

    label = _(u'Edit CollectionMultiView portlet')
    description = _(u"This portlet display a listing of items from a" +
                        " Collection, using custom views")

