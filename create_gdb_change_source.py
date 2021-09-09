# This script is to automate the process of creating one deliverable gdb to the client
# The last part of the script is in case the map needs to be shared as a web map (projection bulk change)
import arcpy

# make the env overwritable
arcpy.env.overwriteOutput = True

# variables
PROJECT = r"D:\LPA\Project\MyProject\MyProject.aprx"
WORKSPACE = "D:\LPA\Project\MyProject"
srWGS84 = arcpy.SpatialReference("WGS 1984")

# List names of layers
aprx = arcpy.mp.ArcGISProject(PROJECT)
for m in aprx.listMaps():
    print("Map: {0} Layers".format(m.name))
    for lyr in m.listLayers():
        print("  " + lyr.name)
del aprx

# Create a new gdb to send layers
arcpy.CreateFileGDB_management(WORKSPACE, "sd_package")

arcpy.FeatureClassToFeatureClass_conversion()

# Check the projection of all layers
dElement = r"D:\EsriTraining_Past\SADistance\SanDiego.gdb"
desc = arcpy.Describe(dElement)
for child in desc.children:
    if child.dataType == "FeatureDataset":
        pass
    if hasattr(child, "ShapeType"):
        print(f"    {child.name} with projection: {child.spatialReference.name}")
    else:
        pass

# Change the projection of all layers
for child in desc.children:
    arcpy.management.DefineProjection(dElement, srWGS84)