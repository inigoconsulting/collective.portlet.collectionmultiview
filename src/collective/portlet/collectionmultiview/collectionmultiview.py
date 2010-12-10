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
        for attr in ['request','context','data','results',
                     'collection_url','collection']:
            setattr(self,attr,None)

def RendererVocabulary(context):
    fake = FakeRenderer()
    adapters = getAdapters((fake,),ICollectionMultiViewRenderer)
    terms = []
    for name,adapted in adapters:
        terms.append(SimpleVocabulary.createTerm(name))
    return SimpleVocabulary(terms)

alsoProvides(RendererVocabulary,IVocabularyFactory)


class ICollectionMultiView(collection.ICollectionPortlet):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    # some_field = schema.TextLine(title=_(u"Some field"),
    #                              description=_(u"A field to use"),
    #                              required=True)
    renderer = schema.Choice(title=_(u'Renderer'),
                         description=_(u"The name of the Renderer for this portlet."),
                         default='default',
                         required=True,
                         vocabulary='collective.portlet.collectionmultiview.RendererVocabulary')


class Assignment(collection.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ICollectionMultiView)

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u""):
    #    self.some_field = some_field

    def __init__(self, header=u"", target_collection=None, limit=None, random=False, show_more=True, show_dates=False,renderer='default'):
        super(Assignment,self).__init__(header,target_collection,limit,random,show_more,show_dates)
        self.renderer = renderer


class Renderer(collection.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
    implements(ICollectionMultiViewBaseRenderer)

    @property
    def render(self):
        renderer = getattr(self.data,'renderer',None)
        if renderer is None:
           self.data.renderer = 'default'
           renderer = 'default'
        return getAdapter(self,ICollectionMultiViewRenderer,renderer).render


class AddForm(collection.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(ICollectionMultiView)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
    form_fields = form_fields.omit('random', 'show_more', 'show_dates')

    def create(self, data):
        return Assignment(**data)


# NOTE: If this portlet does not have any configurable parameters, you
# can use the next AddForm implementation instead of the previous.

# class AddForm(base.NullAddForm):
#     """Portlet add form.
#     """
#     def create(self):
#         return Assignment()


# NOTE: If this portlet does not have any configurable parameters, you
# can remove the EditForm class definition and delete the editview
# attribute from the <plone:portlet /> registration in configure.zcml


class EditForm(collection.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(ICollectionMultiView)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
    form_fields = form_fields.omit('random', 'show_more', 'show_dates')

