import arcpy
import os
import pythonaddins

class OpenRadarsat(object):
    """Implementation for GEM2Toolbar_addin.tool3 (Tool). """
    # Initialise the tool's cursor functionality
    def __init__(self):
        self.enabled = True
        # Sets the cursor to be a cross
        self.cursor = 3
        # Sets the shape of the object to be drawn by the cursor action
        self.shape = "Rectangle"
    def onRectangle(self, rectangle_geometry):
        # Get the current map document, the first data frame and the shapefile.
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        layers = arcpy.mapping.ListLayers(df)
        sf = [x.name for x in layers if x.name=='Filtered Targets (applied selection criteria)'][0]
        # Get the spatial reference of the data frame
        sr = df.spatialReference
        # Set a polygon from the drawn rectangle and select the features
        poly = makePolyFromExtent(rectangle_geometry, sr)
        arcpy.SelectLayerByLocation_management(sf, 'INTERSECT', poly)
        # loop throught the RsatID column of the selected features, find the RsatID's and open the associated image in the Products folder
        with arcpy.da.SearchCursor(sf, 'RsatID') as cursor:
             for row in cursor:
                 RsatID = row[0]
                 RsatIDvalue = RsatID.lstrip()
                 year = RsatIDvalue.split("_")[5][:4]
                 rasterPath = os.path.join(os.path.dirname(os.path.dirname(mxd.filePath)),"Products",year,RsatIDvalue,"Ortho_8bit","imagery_ortho_8b.tif")
                 rasterLyr = RsatID.lstrip()
                 print 'Adding {} to Data Frame.'.format(rasterLyr)
                 arcpy.MakeRasterLayer_management(rasterPath, rasterLyr)
        # Clear the selection and display the shapefile
        arcpy.SelectLayerByAttribute_management(sf, 'CLEAR_SELECTION')
        arcpy.RefreshTOC()
        arcpy.RefreshActiveView()

class SetLookALike(object):
    """Implementation for GEM2Toolbar_addin.tool1 (Tool). This tool allows the user to use a rectangle selection cursor to select the features that are look-a-likes.
     Once the features are selected, their VISIBLE value is changed to 0. This hides the feature in the layer."""
    def __init__(self):
        # Initialise the tool's cursor functionality
        self.enabled = True
        # Sets the cursor to be a cross
        self.cursor = 3
        # Sets the shape of the object to be drawn by the cursor action
        self.shape = "Rectangle"

    def onRectangle(self, rectangle_geometry):
        # Get the current map document, the first data frame and the shapefile.
        mxd = arcpy.mapping.MapDocument('current')
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        layers = arcpy.mapping.ListLayers(df)
        sf = [x.name for x in layers if x.name=='Filtered Targets (applied selection criteria)'][0]
        # Get the spatial reference of the data frame
        sr = df.spatialReference
        # Set a polygon from the drawn rectangle and select the features
        poly = makePolyFromExtent(rectangle_geometry, sr)
        arcpy.SelectLayerByLocation_management(sf, 'INTERSECT', poly)
        # User prompt to make sure the selected features are the right ones to declare as look-a-likes.
        result = pythonaddins.MessageBox('Click OK to hide the selected feature(s)', 'Visible to Invisible', 1)
        # Loop through the selected features and change the VISIBlE column value to 0
        if result == 'OK':
            with arcpy.da.UpdateCursor(sf,'VISIBLE') as cursor:
                 for row in cursor:
                     row[0]=0
                     cursor.updateRow(row)
        # Clear the selection and display the shapefile
        arcpy.SelectLayerByAttribute_management(sf,'CLEAR_SELECTION')
        arcpy.RefreshActiveView()

class SetDarkFeature(object):
    """Implementation for GEM2Toolbar_addin.tool2 (Tool). This tool allows the user to use a rectangle selection cursor to select the features that are look-a-likes.
     Once the features are selected, their VISIBLE value is changed to 0. This hides the feature in the layer."""
    def __init__(self):
        # Initialise the tool's cursor functionality
        self.enabled = True
        # Sets the cursor to be a cross
        self.cursor = 3
        # Sets the shape of the object to be drawn by the cursor action
        self.shape = "Rectangle"
    def onRectangle(self, rectangle_geometry):
        # Get the current map document, the first data frame and the shapefile.
        mxd = arcpy.mapping.MapDocument('current')
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        layers = arcpy.mapping.ListLayers(df)
        sf = [x.name for x in layers if x.name=='Filtered Targets (applied selection criteria)'][0]
        # Get the spatial reference of the data frame
        sr = df.spatialReference
        # Set a polygon from the drawn rectangle and select the features
        poly = makePolyFromExtent(rectangle_geometry, sr)
        arcpy.SelectLayerByLocation_management(sf, 'INTERSECT', poly)
        # User prompt to make sure the selected features are the right ones to declare as dark features.
        result = pythonaddins.MessageBox('Click OK to unhide the selected feature(s)', 'Invisible to Visible', 1)
        # Loop through the selected features and change the VISIBlE column value to 1
        if result == 'OK':
            with arcpy.da.UpdateCursor(sf,'VISIBLE') as cursor:
                for row in cursor:
                     row[0]=1
                     cursor.updateRow(row)
        # Clear the selection and display the shapefile
        arcpy.SelectLayerByAttribute_management(sf,'CLEAR_SELECTION')
        arcpy.RefreshActiveView()

# Makes a polygon with the rectangle extent from the tool
def makePolyFromExtent(ext, sr):
    """makes an arcpy polygon object from an input extent object.
    Returns a polygon geometry object."""
    array = arcpy.Array()
    array.add(ext.lowerLeft)
    array.add(ext.lowerRight)
    array.add(ext.upperRight)
    array.add(ext.upperLeft)
    array.add(ext.lowerLeft)
    return arcpy.Polygon(array, sr)