import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def sub(image: np.ndarray,x1:int, y1:int, x2:int, y2:int)-> np.ndarray:
    submatrix = [row[x1:x2] for row in image[y2:y1]]
    resized_submatrix = np.resize(submatrix,(y1 - y2, x2 - x1))
    return resized_submatrix

def calculate(matrix: np.ndarray):
    ## Just True point
    count = np.count_nonzero(matrix)
    area = count*0.3*0.3
    print(area)

    ## All point
    rows, cols = matrix.shape
    print(rows*cols*0.3*0.3)

def main(x1: int, x2:int,y1:int,y2:int):
    mask = np.load('mask.npy')
    image = Image.open("my_mask_visualization.png")
    # rotated_image = image.rotate(-90).resize(mask.shape).transpose(Image.FLIP_LEFT_RIGHT)
    # image_array = np.array(rotated_image)
    matrix = sub(image=mask, x1=x1, y1=y1,x2=x2,y2=y2)
    # img = sub(image=image_array, x1=0,y1=12000,x2=2000,y2=10000)
    # calculate_area(image=img, mask=matrix)
    calculate(matrix=matrix)
    plt.pcolormesh(matrix, cmap="binary")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("2D Array Visualization")
    plt.show()

if __name__=="__main__":
    main(x1=0, y1=12000,x2=2000,y2=10000)