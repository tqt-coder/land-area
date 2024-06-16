import os
import cv2
import numpy as np
import imageio as iio
import matplotlib.pyplot as plt

def calculate_area(image, mask):
	unique_values, counts = np.unique(image[mask], return_counts=True)
	area={}
	for i in range(len(unique_values)):
		area[unique_values[i]] = (counts[i]*0.2986*0.2986)/1000000
	return area

def open_img(root: str) -> np.ndarray:
    """
    Because cv2 doesn't know unicode link, we use iio

    Args:
        root: str
            path of img
    
    Returns:
        img
    """
    root = root.replace("\\","\\\\")
    if not os.path.exists(root):
        print(f"File does not exist: {root}")
        return False
    else:
        try:
            image = iio.imread(root)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            return image
        except Exception as e:
            print(f"Failed to read the image with imageio: {e}")
            return False


def merging_row(index, folder_path, flag=True):
    color_ranges = {        
        0: [255, 255, 255],
        1: [0,0,255],
        2: [0,255,255],
        3: [255,0,0],
        4: [183, 129, 159],
        5: [0,255,0],
        6: [128, 195, 255],
    }
    flaw_size = np.array([39, 38, 37, 36, 35, 34, 33, 32, 23, 22, 21, 20, 19, 18, 17, 16, ])

    img_path = os.path.join(folder_path, str(index[0])+".png")
    image_row = open_img(root=img_path)
    if flag == True:
        image_row = cv2.resize(image_row,(1926, 1825))
    else:
        image_row = cv2.resize(image_row,(1926, 1824))
    image_row = encode_image_to_1d(image_row, color_ranges)
    x=0
    for i in index[1:]:
        image_path = os.path.join(folder_path, str(i)+".png")
        image = open_img(root=image_path)
        try:
            new_image = cv2.resize(image,(1926, 1824))
            new_image = encode_image_to_1d(new_image, color_ranges)
            new_image_row = np.concatenate((image_row, new_image), axis=1)
            x+=1
        except:
            new_image = cv2.resize(image,(1926, 1825))
            new_image = encode_image_to_1d(new_image, color_ranges)
            new_image_row = np.concatenate((image_row, new_image), axis=1)
    print(f"Num is {x}")
    return new_image_row

def encode_image_to_1d(image, color_ranges):
  """
  Encodes an image with specified color ranges to a 1D array with label values (0-6).

  Args:
      image: A 3D NumPy array representing the image (height, width, channels).
      color_ranges: A dictionary mapping label names to tuples of color ranges (BGR).

  Returns:
      A 1D NumPy array containing label values (0-6)    for each pixel in the image.
  """

  # Create an empty encoded image to store label values (0 to 6)
  img_classes = np.zeros_like(image)[:, :, 0]  # Initialize with first channel
  unique_colors = set()
  for label, rgb in color_ranges.items():
    img_classes[(image==rgb).all(axis=2)] = label
    unique_values, counts = np.unique(img_classes, return_counts=True)
    
  unique_values, counts = np.unique(img_classes, return_counts=True)
  print(unique_values, counts)

  return img_classes
def get_area_total():
    mask = np.load('mask.npy').reshape(14598, 15408)
    folder_path = "annotations"
    index1=[i for i in range(56,64)]
    index2=[i for i in range(48,56)]
    index3=[i for i in range(40,48)]
    index4=[i for i in range(32,40)]
    index5=[i for i in range(24,32)]
    index6=[i for i in range(16,24)]
    index7=[i for i in range(8,16)] 
    index8 = np.arange(7, -1, -1)
    index = [index1, index2, index3, index4, index5, index6, index7, index8]
    big_images=merging_row(index[0], folder_path=folder_path)
    for i in index[1:]:
        image=merging_row(i, folder_path=folder_path)
        big_images = np.concatenate((big_images, image))
        
    
    # img from 
    plt.imshow(big_images)
    plt.axis('off')
    plt.show()
    print(calculate_area(big_images, mask))
    unique_values, counts = np.unique(mask, return_counts=True)
    print(unique_values, counts)
    total_sum = sum(calculate_area(big_images, mask).values())
    print(total_sum)
    return total_sum