import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from image_downloading import  run
from geo_func import split_polygon, read_geopandas_data

def main():

    #Load geometric data
    geo= read_geopandas_data()
    G = np.random.choice(geo.geometry.values)
    squares   = split_polygon(G,shape='square',thresh=0,side_length=0.005) #thresh is the coverage ratio
    geo_series = gpd.GeoSeries([squares[56], squares[0]]) #choosing top-left and bottom-right squares

    # Create a figure and an axes object.
    fig, ax = plt.subplots()
    #Display the GeoSeries object on the axes object.
    geo_series.plot(color = 'red', ax=ax)
    geo.exterior.plot(color='blue', ax= ax)
    plt.show()


    for idx, bound in enumerate(geo_series):
        #run func for downloading images and saving them
        #run(idx=idx,bound=bound.bounds)
        pass


if __name__ == "__main__":
    main()