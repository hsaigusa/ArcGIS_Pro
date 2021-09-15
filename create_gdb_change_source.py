# This script is to automate the process of creating one deliverable gdb to the client
# The last part of the script is in case the map needs to be shared as a web map (projection bulk change)
import arcpy

# make the env overwritable
arcpy.env.overwriteOutput = True

# variables
project = r"D:\LPA\Project\MyProject\MyProject.aprx"
workSpace = "D:\LPA\Project\MyProject"
srWGS84 = arcpy.SpatialReference("WGS 1984")

# Check the current connection of the layers
aprx = arcpy.mp.ArcGISProject(project)
mapx = aprx.listMaps()[0]
for lyr in mapx.listLayers():
    if lyr.supports("DATASOURCE"):
        print(f"{lyr.name}: {lyr.connectionProperties}")


# Create a new gdb to send layers to it
arcpy.CreateFileGDB_management(workSpace, "sd_package")
newSource = "D:\LPA\Project\MyProject\sd_package.gdb"

# Change the all layer sources to the new gdb
for lyr in mapx.listLayers():
    if lyr.supports("DATASOURCE"):
        arcpy.FeatureClassToFeatureClass_conversion(lyr.dataSource,newSource,lyr.name)
        origConnection = lyr.connectionProperties
        newConnection = {'connction_info': {'database': newSource},
                         'workspace_factory': 'File Geodatabase',
                         'dataset': lyr}
        lyr.updateConnectionProperties(origConnection, newConnection)
        print(f"{lyr.name} new connection:{lyr.connectionProperties}")

# Delete project object
del aprx,mapx