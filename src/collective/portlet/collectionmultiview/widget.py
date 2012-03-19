from zope.app.form.browser.widget import SimpleInputWidget
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.formlib import form
from zope.formlib.widget import BrowserWidget, InputWidget
from zope.component import getAdapter
from collective.portlet.collectionmultiview.interfaces import (
    ICollectionMultiViewRenderer
)

class RendererSelectWidget(SimpleInputWidget):

    template = ViewPageTemplateFile('rendererselectwidget.pt')

    def __call__(self):
        value = self._getFormValue()
        return self.template(
            field=self.context,
            name=self.name,
            value=value,
            script=self.script(),
        )

    def script(self):
        return '''
        var reloadRenderer = function () {
            $('[name="%(name)s.reload"]').click();
        }
        ''' % {'name':self.name}
