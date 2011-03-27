Introduction
============

The collectionmultiview portlet is a collection portlet which supports multiple 
view modes. It inherits the built-in plone.portlet.collection and extend it with
view adapters support.

Writing additional views
========================

Creating an additional view is as simple as writing a class which inherits 
from CollectionMultiViewBaseRenderer, and register it as a named adapter

Sample code::

    from collective.portlet.collectionmultiview.renderers.base import (
                                        CollectionMultiViewBaseRenderer)
    from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
  
    class MyCustomRenderer(CollectionMultiViewBaseRenderer):
        __name__ = 'My Custom Renderer'
        template = ViewPageTemplateFile('path/to/template.pt')

ZCML::

  <configure
     xmlns="http://namespaces.zope.org/zope">

     <adapter name="mycustomrenderer"
         factory=".package.MyCustomRenderer"/>

  </configure>
