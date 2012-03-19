from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from collective.portlet.collectionmultiview import BaseRenderer

try:
    from plone.app.discussion.interfaces import IConversation, IDiscussionLayer
    HAS_PAD = True
except ImportError:
    HAS_PAD = False

class SummaryRenderer(BaseRenderer):
    """ display as a summary listing """

    title = 'Summary Renderer'
    template = ViewPageTemplateFile('templates/summary.pt')

    def comment_count(self, obj):
        """
        Returns the number of comments for the given object or False if
        comments are disabled.
        """

        if HAS_PAD:
            if IDiscussionLayer.providedBy(self.request):
                conversation = IConversation(obj)
                return conversation.enabled() and len(conversation)
        if self.context.portal_discussion.isDiscussionAllowedFor(obj):
            discussion = self.context.portal_discussion.getDiscussionFor(obj)
            return discussion.replyCount(obj)
        return False
