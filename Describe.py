import arcpy

# Data to be described
dElement = r"D:\EsriTraining_Past\SADistance\SanDiego.gdb"
desc = arcpy.Describe(dElement)

# Print the name of the data elements, including Child data
print(f"Describing {dElement}...")
print("Name:        " + desc.name)
print("Dtype:     " + desc.dataType)
print("CatalogPath:        " + desc.catalogPath)
print("Children:")
for child in desc.children:
    if child.dataType == "FeatureDataset":
        pass
    if hasattr(child, "ShapeType"):
        print(f"    with Extent: {child.extent} and projection: {child.spatialReference.name}")
    else:
        print(f"  {child.name} is a {child.dataType}")
    print("   and Fields:")
    for field in child.fields:
        print(f"  {field.name} is a {field.type}")

print("\nScript finished");