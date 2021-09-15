import arcpy.

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