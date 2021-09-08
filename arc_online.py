#import arcgis
from arcgis.gis import GIS
from secret import inf_arc

gis = GIS(inf_arc[0], inf_arc[1], inf_arc[2])

# Users
user = gis.users.get(inf_arc[1])
print(user.lastName)

# contents_search
items = gis.content.search('San Diego')
for item in items:
    print(item)