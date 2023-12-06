import arcpy
from arcpy import env

# Set workspace environment
env.workspace = r"G:\Geodatabase\Water.gdb"  # Update with your actual geodatabase path

# Input feature classes to be clipped
input_feature_classes = ["feature_class1", "feature_class2", "feature_class3"]  # Add more feature classes if needed

# Polygon feature class used for clipping
clip_polygon = "P:\ArcGIS Projects\Explore Data\scratch.gdb\Area"

# Output folder for the clipped feature classes
output_folder = r"C:\path\to\output\folder"  # Update with your desired output folder path

# Loop through each input feature class and perform clip
for feature_class in input_feature_classes:
    output_feature_class = arcpy.ValidateTableName(f"{feature_class}_clipped", output_folder)
    arcpy.Clip_analysis(feature_class, clip_polygon, output_feature_class)
    print(f"{feature_class} clipped to {clip_polygon} and saved as {output_feature_class}")

print("Batch clipping process completed.")