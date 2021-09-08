import arcpy

arcpy.env.overwriteOutput = True

# List names of layers
aprx = arcpy.mp.ArcGISProject(r"D:\LPA\Project\MyProject\MyProject.aprx")
for m in aprx.listMaps():
    print("Map: {0} Layers".format(m.name))
    for lyr in m.listLayers():
        print("  " + lyr.name)
del aprx

# Create a new gdb to send layers
arcpy.CreateFileGDB_management("D:\LPA\Project\MyProject", "sd_package")

arcpy.FeatureClassToFeatureClass_conversion()

# Check the projection of all layers

# Change the projection of all layers