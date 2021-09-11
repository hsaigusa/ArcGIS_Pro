import arcpy
arcpy.env.overwriteOutput = True

# Project, map, layout and map frame objects
aprx = arcpy.mp.ArcGISProject(
    r"D:\LPA\Projects\BookmarkProject\BookmarkProject.aprx")
mapx = aprx.listMaps()[0]
lyt = aprx.listLayouts()[0]
mf = lyt.listElements('MAPFRAME_ELEMENT',"Map Frame")[0]

# Assign layer class to be written - preparing data
defaultGDB = aprx.defaultGeodatabase
bmFCName = "bmFC"
bmFC = fr"{defaultGDB}\{bmFCName}"
sr = arcpy.SpatialReference("WGS 1984 Web Mercator (auxiliary Sphere)")

# Create a feature with the information written above
arcpy.CreateFeatureclass_management(defaultGDB,
                                    bmFCName,
                                    "POLYGON",
                                    spatial_reference=sr)
arcpy.AddField_management(bmFC,"Name","TEXT","","",50)

cursor = arcpy.da.InsertCursor(bmFC,["SHAPE@","Name"])
array = arcpy.Array()
for bm in mapx.listBookmarks():
    print(bm.name)
    mf.zoomToBookmark(bm)
    extent = mf.camera.getExtent()
    array.add(arcpy.Point(extent.XMin,extent.YMin))
    array.add(arcpy.Point(extent.XMin, extent.YMax))
    array.add(arcpy.Point(extent.XMax,extent.YMax))
    array.add(arcpy.Point(extent.XMax, extent.YMin))
    #To close the polygon, add the first point again
    array.add(arcpy.Point(extent.XMin, extent.YMin))
    cursor.insertRow([arcpy.Polygon(array), bm.name])
    print(array,cursor)
    array.removeAll()
del bm,array, cursor, aprx