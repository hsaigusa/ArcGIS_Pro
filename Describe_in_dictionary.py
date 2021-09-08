import arcpy

# Data to be described
dElement = r"D:\EsriTraining_Past\SADistance\Otay.gdb"

# Print Element with number, key, value
descDict = arcpy.da.Describe(dElement)
for i, key in enumerate(descDict):
    print(f"{i+1},{key},{descDict[key]}")

print("script finished")