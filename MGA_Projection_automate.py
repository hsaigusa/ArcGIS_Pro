import arcpy
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

# Create Spatial Reference object for the places layer which will be
# the geographic coordinate system of the source feature class
srPlacesLayer = arcpy.Describe(placesLayer).SpatialReference

# Write one PDF page for each place in the sorted list
# Use slice notation to only do the first 10 olaces in the list
for pageCount, placeName in enumerate(placeSortedByNameList[:10]):
    