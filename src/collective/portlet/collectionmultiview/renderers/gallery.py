from base import CollectionMultiViewBaseRenderer
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from Acquisition import aq_inner


class GalleryRenderer(CollectionMultiViewBaseRenderer):

     template = ViewPageTemplateFile('skins/gallery.pt')

     def square_tile(self,obj,scale='tile',css_class='tileImage'):
         context = aq_inner(obj)
         # test for leadImage and normal image
         for fieldname in ['leadImage','image']:
             field = context.getField(fieldname)
             if field is not None:
                image = field.getRaw(context)
                
     #FIXME: This should be shared across site as a plonetool
     def cropcenter(self,data,format="PNG"):
        img = Image.open(StringIO(data))
        # resize to width or height, whichever smaller

        # if width is smaller
        if img.size[0] < img.size[1]:
           # calculate newheight and scale
           ratio = float(img.size[0])/self.size[0]
           height = int(img.size[1]/ratio)
           imgout = img.resize((self.size[0],height))
        else:
           # calculate newwidth and scale
           ratio = float(img.size[1])/self.size[1]
           width = int(img.size[0]/ratio)
           imgout = img.resize((width,self.size[1]))

        center = (imgout.size[0]/2,imgout.size[1]/2)

        # find start and end point
        cropstart = (center[0] - self.size[0]/2,center[1] - self.size[1]/2)
        cropend = (center[0] + self.size[0]/2,center[1] + self.size[1]/2)

        # check for overflow
        if cropstart[0] < 0: cropstart[0] = 0
        if cropstart[1] < 0: cropstart[1] = 0
        if cropend[0] > imgout.size[0]: cropend[0] = imgout.size[0]
        if cropend[1] > imgout.size[1]: cropend[1] = imgout.size[1]

        imgout = imgout.crop((cropstart[0],cropstart[1],
                              cropend[0],cropend[1]))
        outio = StringIO()
        imgout.save(outio,format)
        outio.seek(0)
        buffer = outio.read()

        return buffer

