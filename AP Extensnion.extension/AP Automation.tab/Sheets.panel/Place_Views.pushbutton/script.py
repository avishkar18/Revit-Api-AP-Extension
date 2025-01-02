# -*- coding: utf-8 -*-
__title__ = "Place Views"
__doc__ = """Version = 1.0
Date    = 01.11.2024
_____________________________________________________________________
Description:
Create Sheet and Place views on Appropriate sheet Automaticaly.
_____________________________________________________________________
How-to:
-> Click on the button
-> ...
_____________________________________________________________________
Last update:
- [16.07.2024] - 1.1 Fixed an issue...
- [15.07.2024] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
- Describe Next Features
_____________________________________________________________________
Author: Erik Frits"""

# .NET Imports (You often need List import)
import clr
# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *

# pyRevit
clr.AddReference("System")

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#==================================================
doc   = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app   = __revit__.Application

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝
#==================================================
def find_viewport_id(doc,view_id):
    # Collect all viewports in the project
    collector = FilteredElementCollector(doc).OfClass(Viewport)

    # Iterate through each viewport and check if its view ID matches the given view ID
    for viewport in collector:
        if viewport.ViewId == ElementId(view_id):
            return viewport

    return None

def get_viewport_size(viewport):                  #gives size of viewport
    # Get the outline of the viewport
    outline = viewport.GetBoxOutline()

    # Get the min and max points of the outline
    min_pt = outline.MinimumPoint
    max_pt = outline.MaximumPoint

    # Calculate the width and height
    width = max_pt.X - min_pt.X
    height = max_pt.Y - min_pt.Y

    return width, height

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
#==================================================
# START CODE HERE

#Get All Views
views=FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
view_names={v.Name:v for v in views}

#Get All Schedules
Schedules=FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Schedules).WhereElementIsNotElementType().ToElements()
schedule_names={v.Name:v for v in Schedules}

# Title Block Name
Title_Blocks= FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks).WhereElementIsElementType().ToElements()
Title_Block= None

name_of_sheet = "ROTF Titleblock-FS"
for block in Title_Blocks:
    block_Name=block.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
    if block_Name==name_of_sheet:
        Title_Block=block
    else:
        continue

print Title_Block
# Get Sheet Id
sheets=FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType().ToElements()
sheet_id=[s.Id for s in sheets if s.Name== "FULL SET"]

# Sheet 1
FS_1_items= ['FURNITURE & EQUIPMENT PLAN',"Furniture Schedule","Door Schedule","AREA PLAN",'DIMENSION & ELECTRICAL PLAN']
FS_1_Views_ids={v.Name:v.Id for v in views if v.get_Parameter(BuiltInParameter.VIEW_NAME).AsString() in FS_1_items}
FS_1_Schedules = {s.Name:s.Id for s in Schedules if s.get_Parameter(BuiltInParameter.VIEW_NAME).AsString() in FS_1_items}
FS_1_viewport_ids={}

# Placing Views And Schedule On Sheet 1

v_width=0
v_height=0
x_co=0
y_co=0
v_x= 0
v_y= 0


t = Transaction(doc, "Create Sheet")
t.Start()
for i in FS_1_items:
    if i in view_names:
        try:
            vp_plan = Viewport.Create(doc, sheet_id[0], view_names[i].Id, XYZ(x_co, y_0co, 0.0))
            FS_1_viewport_ids[vp_plan]=vp_plan.ViewId
            width_height=get_viewport_size(vp_plan)
            v_width=width_height[0]
            v_height=width_height[1]
            if (v_width+0.3)*2 <= 3:
                v_x = (v_width/2) + 0.06
                v_y =2-(v_height/2)-0.06
                vp_plan.SetBoxCenter(XYZ(v_x,v_y,0.0))
            # print v_height, v_width
            break
        except:
            print ("error placing view")
    else:
        try:
            place_schedule= ScheduleSheetInstance.Create(doc, sheet_id[0], schedule_names[i].Id, XYZ(x_co, 1, 0.0))

        except:
            print ("error placing Schedule")
    x_co += 0.3

# Placement Cases
# width_tb=3
# height_tb=2
#
# vp=find_viewport_id(doc,32)
# width_height =get_viewport_size(vp)
# width=width_height[0]
# height=width_height[1]
# print width,height

t.Commit()
print ('Done')