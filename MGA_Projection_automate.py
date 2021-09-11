import arcpy, os
arcpy.env.overwriteOutput = True

# Project object
aprx =  arcpy.mp.ArcGISProject(r"D:\LPA\Projects\MGAZonesProject\MGAZonesProject.aprx")

# Map objects
map54 = aprx.listMaps("Map54")[0]
map55 = aprx.listMaps("Map55")[0]
map56 = aprx.listMaps("Map56")[0]

# Layer object
placesLayer = map54.listLayers("Queensland Places")[0]

# Layout object
lyt = aprx.listLayouts()[0]

# Map Frame Objects
mapFrame54 = lyt.listElements('MAPFRAME_ELEMENT',"Map Frame 54")[0]
mapFrame55 = lyt.listElements('MAPFRAME_ELEMENT',"Map Frame 55")[0]
mapFrame56 = lyt.listElements('MAPFRAME_ELEMENT',"Map Frame 56")[0]

# Spatial Reference Text Objects
srText54 = lyt.listElements('TEXT_ELEMENT', "Spatial Reference 54")[0]
srText55 = lyt.listElements('TEXT_ELEMENT', "Spatial Reference 55")[0]
srText56 = lyt.listElements('TEXT_ELEMENT', "Spatial Reference 56")[0]

# Create PDF Document Object
finalPDF = r"D:\LPA\PDFs\MGAZones.pdf"
if arcpy.Exists(finalPDF):
    arcpy.Delete_management(finalPDF)
pdfDoc = arcpy.mp.PDFDocumentCreate(finalPDF)

# Create list of place names sorted alphabetically
placeSortedByNameList = sorted([
    row[0] for row in arcpy.da.SearchCursor(
    placesLayer,"NAME")])

# Create dictionary of X, Y coordinates for each place
placesCoordsDict = {row[0]:row[1] for row in arcpy.da.SearchCursor(
    placesLayer,["NAME","SHAPE@XY"])}

print(placesCoordsDict)
# Create Spatial Reference object for the places layer which will be
# the geographic coordinate system of the source feature class
srPlacesLayer = arcpy.Describe(placesLayer).SpatialReference

# Write one PDF page for each place in the sorted list
# Use slice notation to only do the first 10 olaces in the list
for pageCount, placeName in enumerate(placeSortedByNameList[:10]):
    xCoord,yCoord = placesCoordsDict[placeName]
    mgaZone = 1 + int((xCoord + 180) / 6)
    print(f"{placeName} is in zone {mgaZone}")
    srMGA = arcpy.SpatialReference(f"GDA2020 MGA Zone {mgaZone}")

    geogFC = fr"{aprx.defaultGeodatabase}\geogFC"
    projFC = fr"{aprx.defaultGeodatabase}\projFC"

    arcpy.CreateFishnet_management(geogFC,
                                   f"{xCoord - 0.25} {yCoord - 0.25}",
                                   f"{xCoord + 0.25} {yCoord + 0.25}",
                                   0.5, 0.5, 1, 1,
                                   geometry_type="POLYGON", labels="NO_LABELS")
    arcpy.DefineProjection_management(geogFC, srPlacesLayer)
    arcpy.Project_management(geogFC,projFC, srMGA)
    projFCExtent = arcpy.Describe(projFC).extent

    if mgaZone == 54:
        mapFrame54.visible = True
        mapFrame54.camera.setExtent(projFCExtent)
        mapFrame54.camera.scale = mapFrame54.camera.scale * 1.05
        mapFrame55.visible = False
        mapFrame56.visible = False
        srText54.visible = True
        srText55.visible = False
        srText56.visible = False
    elif mgaZone == 55:
        mapFrame54.visible = False
        mapFrame55.camera.setExtent(projFCExtent)
        mapFrame55.camera.scale = mapFrame55.camera.scale * 1.05
        mapFrame55.visible = True
        mapFrame56.visible = False
        srText54.visible = False
        srText55.visible = True
        srText56.visible = False
    elif mgaZone == 56:
        mapFrame54.visible = False
        mapFrame56.camera.setExtent(projFCExtent)
        mapFrame56.camera.scale = mapFrame56.camera.scale * 1.05
        mapFrame55.visible = False
        mapFrame56.visible = True
        srText54.visible = False
        srText55.visible = False
        srText56.visible = True
    else:
        print(f"Unexpected zone number of {mgaZone} encountered")

    # Title text object
    titleText = lyt.listElements('TEXT_ELEMENT',"Title")[0]
    titleText.text = placeName

    #Export PDF for this country's page
    lyt.exportToPDF(fr"D:\LPA\PDFs\test{pageCount}.pdf")
    pdfDoc.appendPages(fr"D:\LPA\PDFs\test{pageCount}.pdf")

# Save and close PDF and open in Adobe
pdfDoc.saveAndClose()
del pdfDoc
os.startfile(finalPDF)
# Delete project object
del aprx



