import geopandas as gpd
import numpy as np
from shapely.ops import split
from shapely.geometry import MultiPolygon, LineString

def read_geopandas_data():
    file = 'geometry_data/VNM_adm3.shp' # Path to the shapefile
    # Load the JSON data
    data = gpd.read_file(file)
    data = gpd.GeoDataFrame(data, crs='WGS84')
    dalat= data[data['NAME_2']=='Đà Lạt' ] #chosing a district base on dataset
    Ward=dalat[dalat['NAME_3']=='12'] #choosing a ward of that district
    return Ward['geometry'] 


def get_squares_from_rect(RectangularPolygon, side_length=0.0025):
    """
    Divide a Rectangle (Shapely Polygon) into squares of equal area.

    `side_length` : required side of square

    """
    x1, y1, x2, y2 = RectangularPolygon.bounds
    width = x2 - x1
    height = y2 - y1

    xcells = int(np.round(width / side_length))
    ycells = int(np.round(height / side_length))

    yindices = np.linspace(y1, y2, ycells + 1)
    xindices = np.linspace(x1, x2, xcells + 1)
    horizontal_splitters = [
        LineString([(x, yindices[0]), (x, yindices[-1])]) for x in xindices
    ]
    vertical_splitters = [
        LineString([(xindices[0], y), (xindices[-1], y)]) for y in yindices
    ]
    result = RectangularPolygon
    for splitter in vertical_splitters:
        result = MultiPolygon(split(result, splitter))
    for splitter in horizontal_splitters:
        result = MultiPolygon(split(result, splitter))
    square = []
    for res in result.geoms:
      square.append(res)
    return square


def split_polygon(G, side_length=0.025, shape="square", thresh=0.9):
    """
    Using a rectangular envelope around `G`, creates a mesh of squares of required length.
    
    Removes non-intersecting polygons. 
            

    Args:
    
    - `thresh` : Range - [0,1]

        This controls - the number of smaller polygons at the boundaries.
        
        A thresh == 1 will only create (or retain) smaller polygons that are 
        completely enclosed (area of intersection=area of smaller polygon) 
        by the original Geometry - `G`.
        
        A thresh == 0 will create (or retain) smaller polygons that 
        have a non-zero intersection (area of intersection>0) with the
        original geometry - `G` 

    - `side_length` : Range - (0,infinity)
        side_length must be such that the resultant geometries are smaller 
        than the original geometry - `G`, for a useful result.

        side_length should be >0 (non-zero positive)

    - `shape` : {square/rhombus}
        Desired shape of subset geometries. 


    """
    assert side_length>0, "side_length must be a float>0"
    Rectangle    = G.envelope
    squares      = get_squares_from_rect(Rectangle, side_length=side_length)
    SquareGeoDF  = gpd.GeoSeries(squares)
    SquareGeoDF = SquareGeoDF.set_crs('EPSG:32649')

    Geoms        = SquareGeoDF.geometry
    geoms = [g for g in Geoms if ((g.intersection(G)).area / g.area) >= thresh]
    return geoms
