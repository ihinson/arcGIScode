import arcpy
import os
import zipfile

#Paths (don't change)
output_dir = r"C:\Users\ihinson\Downloads\Unzipped"
clip_feature = r"G:\Geodatabase\Boundaries.gdb\District_Boundry"
output_gdb = r"G:\Geodatabase\Reference_DistrictBoundaries.gdb"

#CHANGE the file path and feature class
zip_file_path = r"C:\Users\ihinson\Downloads\Parcels_-3049768168105982538.zip"
output_feature_class = "Parcels"

# Unzip the file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(output_dir)

# Get the path of the extracted shapefile
extracted_files = zip_ref.namelist()
shapefile_name = None
for file in extracted_files:
    if file.endswith(".shp"):
        shapefile_name = file
        break

if shapefile_name:
    shapefile_path = os.path.join(output_dir, shapefile_name)

    # Check if the feature class exists in the geodatabase
    feature_class_exists = arcpy.Exists(os.path.join(output_gdb, output_feature_class))
    if feature_class_exists:
        # Delete the existing feature class
        arcpy.Delete_management(os.path.join(output_gdb, output_feature_class))

    # Clip the shapefile to the specified boundaries
    arcpy.Clip_analysis(shapefile_path, clip_feature, os.path.join(output_gdb, output_feature_class))

    print(f"Shapefile '{shapefile_name}' has been unzipped and clipped to '{clip_feature}'.")

else:
    print("No shapefile found in the specified ZIP file.")

print("Editor tracking has been enabled on the feature class.")

# Clean up the extracted files
for file in extracted_files:
    file_path = os.path.join(output_dir, file)
    os.remove(file_path)

# Delete the extracted folder
os.rmdir(output_dir)

# Delete the downloaded ZIP file
os.remove(zip_file_path)

print ("zip file removed")

print ("update complete")