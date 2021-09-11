import arcpy
arcpy.env.overwriteOutput = True

# Project, map, layout and map frame objects
aprx = arcpy.mp.ArcGISProject(
    r"D:\LPA\Projects\BookmarkProject\BookmarkProject.aprx")
mapx = aprx.listMaps()[0]
lyt = aprx.listLayouts()[0]
mf = lyt.listElements('MAPFRAME_ELEMENT',"Map Frame")[0]
lyr = mapx.listLayers("bmFC")[0]
mapx.removeLayer = (lyr)

pdfFile = r"D:\LPA\PDFs\BookmarksMapBookNOFC.pdf"
if arcpy.Exists(pdfFile):
    arcpy.management.Delete(pdfFile)
pdfDoc = arcpy.mp.PDFDocumentCreate(pdfFile)

for count, bm in enumerate(mapx.listBookmarks()):
    print(bm.name)
    mf.zoomToBookmark(bm)
    pdfPage = fr"D:\LPA\PDFs\BookmarksMapBookNOFC{count}.pdf"
    lyt.exportToPDF(pdfPage)
    pdfDoc.appendPages(pdfPage)
    arcpy.management.Delete(pdfPage)
pdfDoc.saveAndClose()

del bm, aprx, pdfDoc