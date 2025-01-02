# -*- coding: utf-8 -*-
__title__ = "Check Varies"
__doc__ = """Version = 1.0
Date    = 01.11.2024
_____________________________________________________________________
Description:
This tool creates a duplicate/ Copy of wall with desired width
_____________________________________________________________________
How-to:
-> Click on the button
-> Enter the Thickness/ Width of New Wall
-> Click Confirm Button
_____________________________________________________________________
Last update:
- [15.12.2024] - 1.0 RELEASE
_____________________________________________________________________

Author: Avishkar Patil """


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *

# import clr
import pandas as pd
doc = __revit__.ActiveUIDocument.Document


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#==================================================

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝
schedules= FilteredElementCollector(doc).OfClass(ViewSchedule).ToElements()
schedules_data = {}
for schedule in schedules:
    if schedule.Name == "Operational Equipment Schedule":
        print("Processing Schedule: " + schedule.Name)
        table_data = schedule.GetTableData()
        section_data = table_data.GetSectionData(SectionType.Body)  # Get the body section

        # Initialize a list to hold row data
        rows = []

        # Extract column headers
        headers = []
        for col in range(section_data.NumberOfColumns):
            headers.append(schedule.GetCellText(SectionType.Header, 0, col))

        # Extract row data
        for row in range(section_data.NumberOfRows):
            row_data = []
            for col in range(section_data.NumberOfColumns):
                try:
                    cell_value = schedule.GetCellText(SectionType.Body, row, col)
                    row_data.append(cell_value)
                except Exception as e:
                    row_data.append(None)  # Handle empty or error cells
            rows.append(row_data)

        # Create a Pandas DataFrame for the schedule
        df = pd.DataFrame(rows, columns=headers)

        # Store the DataFrame in a dictionary
        schedules_data[schedule.Name] = df

    # Example: Access a specific schedule's DataFrame
    for name, df in schedules_data.items():
        print("Schedule Name: " + name)
        print(df.head())  # Print the first few rows of the DataFrame

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
#==================================================
# START CODE



