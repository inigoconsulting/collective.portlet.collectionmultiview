from collective.portlet.collectionmultiview.interfaces import ICollectionMultiViewBaseRenderer,ICollectionMultiViewRenderer
from zope.component import adapts
from zope.interface import implements, Interface
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from plone.memoize.instance import memoize
from Acquisition import aq_inner

from zope import schema
from collective.portlet.collectionmultiview import CollectionMultiViewMessageFactory as _
try:
    from plone.app.discussion.interfaces import IConversation, IDiscussionLayer
    HAS_PAD = True
except ImportError:
    HAS_PAD = False

class CollectionMultiViewBaseRenderer(object):
#    adapts(ICollectionMultiViewBaseRenderer)
    adapts(None)
    implements(ICollectionMultiViewRenderer)

    available = True

    def __init__(self, base):
        if base is None:
            """ hack to allow us to query for all adapters """
            return

        self.request = base.request
        self.context = aq_inner(base.context)
        self.data = base.data
        self.results = base.results
        self.collection_url = base.collection_url
        self.collection = base.collection
        self.base = base

    def render(self, *args, **kwargs):
        return self.template(*args, **kwargs)

    def tag(self, obj, scale='tile', css_class='tileImage'):
        context = aq_inner(obj)
        # test for leadImage and normal image
        for fieldname in ['leadImage','image']:
            field = context.getField(fieldname)
            if field is not None:
                if field.get_size(context) != 0:
                    return field.tag(context, scale=scale, css_class=css_class)
        return ''

class IDefaultSchema(Interface):
    random = schema.Bool(
        title=_(u"Select random items"),
        description=_(u"If enabled, items will be selected randomly from the "
                      u"collection, rather than based on its sort order."),
        required=True,
        default=False)

    show_more = schema.Bool(
        title=_(u"Show more... link"),
        description=_(u"If enabled, a more... link will appear in the footer "
                      u"of the portlet, linking to the underlying "
                      u"Collection."),
        required=True,
        default=True)

    show_dates = schema.Bool(
        title=_(u"Show dates"),
        description=_(u"If enabled, effective dates will be shown underneath "
                      u"the items listed."),
        required=True,
        default=False)



class DefaultRenderer(CollectionMultiViewBaseRenderer):

    __name__ = 'Default Renderer'
    schema = IDefaultSchema
    template = ViewPageTemplateFile('skins/default.pt')

class BlogRenderer(CollectionMultiViewBaseRenderer):

    __name__ = 'Blog Renderer'

    template = ViewPageTemplateFile('skins/blog.pt')

class ColumnRenderer(CollectionMultiViewBaseRenderer):

    __name__ = 'Column Renderer'

    template = ViewPageTemplateFile('skins/column.pt')

class SummaryRenderer(CollectionMultiViewBaseRenderer):

    __name__ = 'Summary Renderer'

    template = ViewPageTemplateFile('skins/summary.pt')

    def comment_count(self, obj):
        """
        Returns the number of comments for the given object or False if
        comments are disabled.
        """
        
        if HAS_PAD:
            if IDiscussionLayer.providedBy(self.request):
                conversation = IConversation(obj)
                return conversation.enabled() and len(conversation)
        if self.portal_discussion.isDiscussionAllowedFor(obj):
            discussion = self.portal_discussion.getDiscussionFor(obj)
            return discussion.replyCount(obj)
        return False
