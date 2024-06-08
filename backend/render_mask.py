import time
import numpy as np
import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
from image_downloading import image_size
from Satellite_Image_Collector import split_polygon
from Satellite_Image_Collector import read_geopandas_data
from matplotlib.path import Path



start = time.time()
geo = read_geopandas_data()
G = np.random.choice(geo.geometry.values)

squares = split_polygon(G, shape='square', thresh=0, side_length=0.005)
geo_series = gpd.GeoSeries(squares)

tf_lon, _, _, tf_lat = geo_series[56].bounds
_, br_lat, br_lon, _ = geo_series[0].bounds
"""print(tf_lon, tf_lat, br_lon, br_lat)
plt.plot(br_lon, br_lat, 'go')
plt.plot(tf_lon, tf_lat, 'ro')"""


W, H = image_size(tf_lat, tf_lon, br_lat, br_lon, zoom=19)
print(W,H)
dx = (br_lon-tf_lon)/W
dy = (tf_lat-br_lat)/H

valuesx = np.arange(0, W)
oney = np.ones((1,H), dtype=int)
image_dx = valuesx.reshape((W,1))*oney

valuesy = np.arange(H,0, -1)
onex = np.ones((W,1), dtype=int)
image_dy = valuesy.reshape((1,H))*onex

lon = np.add(image_dx*dx, tf_lon)
lat = np.add(image_dy*dy, br_lat)

area = {}

boundary = Polygon(geo_series[geo_series.index[0]])

path = Path(list(boundary.exterior.coords))  # Create Path from Polygon's vertices


def is_point_inside_polygon(point):
    return path.contains_point(point)

mask = np.full(lat.shape, False, dtype=bool)
# Check if point is inside the polygon
#mask = np.array([[is_point_inside_polygon((lon[i][j], lat[i][j])) for j in range(W)] for i in range(H)], dtype=bool)
print(lon.shape, lat.shape)
for i in range(W):
    if(i%500 == 0):
        print(time.time()-start)
    for j in range(H):
        mask[i,j] = is_point_inside_polygon((lon[i][j], lat[i][j]))


unique_values, counts = np.unique(mask, return_counts=True)

np.save("mask", mask)  # Corrected filename
end = time.time()
print(end - start)
plt.pcolormesh(mask.reshape(W, H), cmap="binary")  # Reshape for plotting

# Optional: Add labels and title
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("2D Array Visualization")
plt.savefig("my_mask_visualization.png")