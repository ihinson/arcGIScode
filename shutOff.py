import arcpy
import os, sys
from zipfile import ZipFile
import xlrd
import openpyxl
import arcpy
from datetime import datetime
import calendar
from arcgis.gis import GIS
from arcgis import features
from arcgis.features import FeatureLayerCollection
import pandas as pd
import openpyxl

#Get the current month as a number 
current_month_number = datetime.now().month

print(current_month_number)

#Convert the current month to word
current_month_name = calendar.month_name[current_month_number]

print(current_month_name)

#Get entry count
wb = openpyxl.load_workbook(f"G:\Shutoffs\ShutOffs_{current_month_name}.xlsx")
ws = wb.active

count = 0
for row in ws:
    if not all([cell.value == None for cell in row]):
        count += 1
entries = count - 1
print(entries)

# set the current workspace & set overwrite options
arcpy.env.overwriteOutput = True

# conversion
input_excel = fr"G:\Shutoffs\ShutOffs_{current_month_name}.xlsx" 
output_table = fr"G:\Shutoffs\GIS\WaterShutoffs.gdb\WaterShutoffs_Table_{current_month_name}"

arcpy.conversion.ExcelToTable(input_excel, output_table, "Sheet1", 1, '')

print("Conversion completed sucessfully")

# The qualifiedFieldNames environment is used by Copy Features when persisting the join field names.
arcpy.env.qualifiedFieldNames = False

# Set local variables
# !!! change inFeatures when changing meters
inFeatures = f"G:\Shutoffs\GIS\WaterShutoffs.gdb\CustomerMeters"
joinTable = output_table
joinField = "Account_full"
outFeature = f"G:\Shutoffs\GIS\WaterShutoffs.gdb\Shutoffs_{current_month_name}"

# Join the feature layer to a table
joined_table = arcpy.management.AddJoin(inFeatures, joinField, joinTable, 
                                            joinField)

# Copy the layer to a new permanent feature class
result = arcpy.management.CopyFeatures(joined_table, outFeature)

#COUNT MATCHES
# Set the name of the field for which you want to count non-null values
fc_table_name = result
field_name = "Status"

# Initialize a counter
count_non_null = 0

# Use SearchCursor to iterate through rows
with arcpy.da.SearchCursor(fc_table_name, [field_name]) as cursor:
    for row in cursor:
        # Check if the field value is not null
        if row[0] is not None:
            count_non_null += 1

print(fr"Excel file had {entries}. Feature class had {count_non_null} matches.")

if count_non_null != entries:
    print("Matching error") 

# #CREATE FEATURE CLASS

# #Put in error trapping in case an error occurs when running tool

# in_fc = fr"G:\Shutoffs\GIS\WaterShutoffs.gdb\Shutoffs_{current_month_name}"
# out_lyr = fr"G:\Shutoffs\GIS\WaterShutoffs.gdb\Shutoffs_{current_month_name}"

# try:
#     arcpy.MakeFeatureLayer_management(in_fc,out_lyr)
# except:
#     print(arcpy.GetMessages())


#  Description: Use TableToTable with an expression to create a subset
#  of the original table.
  
# Set environment settings
arcpy.env.workspace = "G:\Shutoffs"
 
# Set local variables
inTable = "G:\Shutoffs\GIS\WaterShutoffs.gdb\Shutoffs_November"
outTable = f"G:\Shutoffs\GIS\Tables\{current_month_name}.csv"
 
# Run TableToTable
arcpy.conversion.ExportTable(inTable, outTable)


#UPDATE HOSTED FEATURE LAYER



# arcpy.env.overwriteOutput = True

# updated_fc = result
# gis = GIS('https://mukilteowwd.maps.arcgis.com/', 'ihinson@mukilteowwd.org', 'Arcremind08!', verify_cert=True)
# hosted_fc = "91651bdfd66f4d5aab54289ebfec520e"

# featureService = True                                         
# hostedTable = False                                          
# layerIndex = 0                                              
# disableSync = True                                            
# updateSchema = True  

# #Overwrite hosted feature layer
# dataitem = gis.content.get(hosted_fc)
# fc_coll = FeatureLayerCollection.fromitem(hosted_fc)
# fc_coll.manager.overwrite(updated_fc)

# print ("Update complete.Yay!")

# # # #Write the selected features to a new featureclass
# # # arcpy.CopyFeatures_management(out_lyr, out_lyr)

# # # in_features = f"GIS\WaterShutoffs.gdb\Shutoffs_{current_month_name}"
# # # where_clause = None
# # # in_layer = f"GIS\Shutoffs_{current_month_name}"
# # # out_layer_file = f"GIS\Shutoffs_{current_month_name}.lyrx"

# # # #Run MakeFeatureLayer
# # # arcpy.management.MakeFeatureLayer(in_features, f"Shutoffs_{current_month_name}", where_clause)

# # # #Run SaveToLayerFile
# # # arcpy.management.SaveToLayerFile(f"Shutoffs_{current_month_name}", out_layer_file, "ABSOLUTE")

# # # print("Layer created.")