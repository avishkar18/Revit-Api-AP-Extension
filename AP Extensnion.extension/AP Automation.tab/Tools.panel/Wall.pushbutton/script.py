# -*- coding: utf-8 -*-
__title__ = "Duplicate Wall"
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
import re
import wpf
import clr
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")
clr.AddReference("WindowsBase")
from System.Windows import Application, Window

from pyrevit import script
xamlfile=script.get_bundle_file("ui.xaml")

# WPF window
class MyWindow(Window):
    def __init__(self):
        # Load the XAML file
        wpf.LoadComponent(self,xamlfile)

        # Add event handler for the Confirm button
        self.ConfirmButton.Click += self.on_confirm_click

    def on_confirm_click(self, sender, e):
        # Access the value from the TextBox
        self.wall_width = self.WidthTextBox.Text
        self.Close()


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#==================================================
doc   = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app   = __revit__.Application

t=Transaction(doc, "wall width")
# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝

def get_all_wall_names(doc):
    collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsElementType()
    wall_names = []
    for wall_type in collector:
        name_param = wall_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM)
        if name_param:
            wall_names.append(name_param.AsString())
    return wall_names

def rename(input_string, new_value):   #THIS FUNCTION TAKES STRING VALUE AND RENAMES IT
    if re.search(r'\b\d+(\.\d+)?\b', input_string):
        return re.sub(r'\b\d+(\.\d+)?\b', str(new_value), input_string)
    else:
        return input_string + " - " + str(new_value)+'"'


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
#==================================================
# START CODE HERE

wall_names=get_all_wall_names(doc)
# Get the selected elements
selected_ids = uidoc.Selection.GetElementIds()
# Convert the selected element IDs to elements
selected_elements = [doc.GetElement(id) for id in selected_ids]

window = MyWindow()
window.ShowDialog()  # Show the window in modal mode

#**************** ENTRIES FOR WIDTH AND LAYERS **********
old_width=0
new_width=float(window.wall_width)
finish1=1
finish2=1
structure=float(new_width-finish1-finish2)/12


for i in selected_elements:
    category_element= i.LookupParameter("Category").AsValueString().lower()
    wall_name=i.Name
    suffix=str(new_width)

    if category_element=="walls":
        new_name = rename(wall_name, suffix)
        if new_name in wall_names:
            print new_name + " Name already Exists Try Different Size"
        else:
            wall_type= i.WallType
            t.Start()
            d_wall=wall_type.Duplicate(new_name)     #Duplicates wall type and renames
            t.Commit()

            old_width= d_wall.Width * 12
            compound_structure= d_wall.GetCompoundStructure()
            wall_layers= compound_structure.GetLayers()
            compound_structure.SetLayerWidth(1,structure)
            t.Start()
            d_wall.SetCompoundStructure(compound_structure)
            t.Commit()
            print "Duplicate wall - " + new_name +" created"

    else:
        print ("You Selected wrong Element: Please Select a wall")

