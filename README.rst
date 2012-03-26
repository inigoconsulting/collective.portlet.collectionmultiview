Introduction
============

The collectionmultiview portlet is a collection portlet which supports multiple 
view modes. It inherits the built-in plone.portlet.collection and extend it with
view adapters support.

Writing additional views
========================

Creating an additional view is as simple as writing a class which inherits 
from BaseRenderer, and register it as a named adapter

Sample code::

    from collective.portlet.collectionmultiview import BaseRenderer
    from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
  
    class MyCustomRenderer(BaseRenderer):
        title = 'My Custom Renderer'
        template = ViewPageTemplateFile('path/to/template.pt')

ZCML::

  <configure
     xmlns="http://namespaces.zope.org/zope">

     <adapter name="mycustomrenderer"
         factory=".package.MyCustomRenderer"/>

  </configure>


Extending portlet schema
=========================

You can also extend the portlet schema with additional fields by setting the 
'schema' attribute in the renderer class.

Sample code::

    from collective.portlet.collectionmultiview import BaseRenderer
    from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

    from zope import schema
    from zope.interface import Interface
    from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget

    class IExtraFields(Interface):
        my_extra_field = schema.Text(title=u'Extra field')

    class MyCustomRenderer(BaseRenderer):
        title = 'My Custom Renderer'
        
        schema = IExtraFields
        template = ViewPageTemplateFile('path/to/template.pt')


        #optional 
        custom_widgets = {
            'my_extra_field': WYSIWYGWidget
        }
