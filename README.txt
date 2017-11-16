GEM2Toolbar
===========
This is the GEM2Toolbar add-in used in the Visualisation map step of the GEM2 process.
Developed by Philippe Muise, November 2017 using the 'Python Add-In Wizard'.
MANIFEST
--------

README.txt   : This file

makeaddin.py : A script that will create a .esriaddin file out of this 
               project, suitable for sharing or deployment

config.xml   : The AddIn configuration file. Any changes to the classe names in the install/GEM2Toolbar_addin.py file need to be changed in the config.xml file

Images/*     : all UI images for the project (icons, images for buttons, 
               etc)

Install/*    : The Python project used for the implementation of the
               AddIn entitled GEM2Toolbar_addin.py. This is the python script to be used as the root
               module specified in config.xml.

Features
--------
There are three tools (classes) installed in the toolbar:
1 - SetLookAlike: This tool changes the value in the VISIBLE column of the the main dark feature shapefile to be 0.
The dark features layer in the visualisation map is queried to hide VISIBLE values that are not 1 and will hide the features once selected.
2 - SetDarkFeature: Reverses the actions by SetLookALike. It changes the VISIBLE value of the selected features to 1. 
In order for this tool to be used, the definition query on this layer needs to be changed so that features with a VISIBLE value of 0 are not hidden.
3 - OpenRadarsat: This tool opens the Radarsat 2 image that the dark feature is built off. The Radarsat 2 image selected has been masked to remove land. 


Installation
------------
1 - Double-click the 'makeaddin.py' script to run it. 
2 - Double-click the 'GEM2Toolbar.esriaddin' file to install the add-in to arcmap
3 - In ArcMap, click click the 'Customize' dropdown in menu toolbar, and click on 'Add-In Manager...' The 'GEM2 Toolbar' should be present under 'My Add-Ins'.
4 - Click on 'Customize', then make sure that the GEM2 Toolbar checkbox is selected.
5 - At this point, a toolbar entitle 'GEM2Toolbar' should be visible in your arcmap program. It will remain visible until deselected in the customize list. 

Resources
---------
The 'Python Add=In Wizard is found at: https://www.arcgis.com/home/item.html?id=5f3aefe77f6b4f61ad3e4c62f30bff3b

For additional information on installation, modification, and/or development, the arcgis website provides a good background in their help pages:
http://desktop.arcgis.com/en/arcmap/latest/analyze/python-addins/what-is-a-python-add-in.htm

