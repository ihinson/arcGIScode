import arcpy
import pandas as pd
import os

# List of feature classes
feature_classes = [
    r'G:\Geodatabase\Assets.gdb\Generators',
    r'G:\Geodatabase\Assets.gdb\LaterlFittings',
    r'G:\Geodatabase\Assets.gdb\Lift_Stations',
    r'G:\Geodatabase\Assets.gdb\Pumps',
    r'G:\Geodatabase\Assets.gdb\TP_Assets',
    r'G:\Geodatabase\Assets.gdb\Vehicles_And_Equipment',
    r'G:\Geodatabase\Assets.gdb\Water_Airvacs',
    r'G:\Geodatabase\Assets.gdb\Water_BackFlowAssemblies',
    r'G:\Geodatabase\Assets.gdb\Water_BGSampleStations',
    r'G:\Geodatabase\Assets.gdb\Water_Blowoffs',
    r'G:\Geodatabase\Assets.gdb\Water_Hydrants',
    r'G:\Geodatabase\Assets.gdb\Water_Interties',
    r'G:\Geodatabase\Assets.gdb\Water_MasterMeters',
    r'G:\Geodatabase\Assets.gdb\Water_Meters',
    r'G:\Geodatabase\Assets.gdb\Water_PressureZones',
    r'G:\Geodatabase\Assets.gdb\Water_PRV',
    r'G:\Geodatabase\Assets.gdb\Water_Reservoirs',
    r'G:\Geodatabase\Assets.gdb\Water_SampleStations',
    r'G:\Geodatabase\Assets.gdb\Water_Valves'
]

# Output folder where Excel files will be saved
output_folder = r'S:\Assets'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Export tables as Excel files
for feature_class in feature_classes:
    # Get the name of the table from the full path
    table_name = os.path.basename(feature_class)
    # Export the table to a temporary CSV file
    temp_csv = os.path.join(output_folder, f'{table_name}.csv')
    arcpy.TableToTable_conversion(feature_class, output_folder, f'{table_name}.csv')
    # Convert the CSV file to an Excel file
    df = pd.read_csv(temp_csv)
    excel_file = os.path.join(output_folder, f'{table_name}.xlsx')
    df.to_excel(excel_file, index=False)
    # Remove the temporary CSV file
    os.remove(temp_csv)

print("Tables exported successfully.")