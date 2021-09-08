import arcpy

aprx = arcpy.mp.ArcGISProject(r"D:\LPA\Project\MyProject\MyProject.aprx")
for m in aprx.listMaps():
    print("Map: {0} Layers".format(m.name))
    for lyr in m.listLayers():
        print("  " + lyr.name)
del aprx
