from zope.interface import implements,alsoProvides
from collective.portlet.collectionmultiview.interfaces import (
    ICollectionMultiViewRenderer
)
from zope.component import getAdapters
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

try:
    from zope.schema.interfaces import IVocabularyFactory
except ImportError:
    # BBB Zope 2.12
    from zope.app.schema.vocabulary import IVocabularyFactory



def RendererVocabulary(context):
    """
        Vocabulary which list out all renderers
    """
    adapters = getAdapters((None, ), ICollectionMultiViewRenderer)
    terms = []
    for name, adapted in adapters:
        if hasattr(adapted, 'title'):
            title = adapted.title
        elif hasattr(adapted, '__name__'): # backward compatibility with 1.x 
            title = adapted.__name__
        else:
            title = name
        terms.append(SimpleVocabulary.createTerm(name, name, title))
    return SimpleVocabulary(terms)

alsoProvides(RendererVocabulary, IVocabularyFactory)
