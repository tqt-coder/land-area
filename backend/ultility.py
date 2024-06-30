from render_report import calculate_area, merging_row
import json
import numpy as np
from Satellite_Image_Collector import get_custom_image, get_npy, save_npy, read_size, check_json
# from render_report import calculate_area
from image_downloading import run, check_dir_tree

def merge_large_img(data: json = {}):
    # Check tree
    if data == {}:
        root = "annotations"
        flag = True
    else:
        anno_keys = ("province", "district", "ward")
        if all(check_json(key, data) for key in anno_keys):
            root,flag = check_dir_tree(dir_tree= ["data","annotations", data['province'], data["district"],data["ward"]])
        else:
            flag = True
            root = data['annotations'].replace("\\","\\\\").replace("/","\\\\")
            print(root)
    try:
        if flag:
            size_path = root.replace("annotations","mask")
            W, H = read_size(root=size_path)

            index = []
            for i in range(H,1, -1):
                index.append([x for x in range(W*i-W, W*i)])
            index.append(np.arange(W-1,-1,-1))
            big_images=merging_row(index[0], folder_path=root)
            for i in index[1:]:
                try:
                    image=merging_row(i, folder_path=root)
                    big_images = np.concatenate((big_images, image))
                except:
                    image=merging_row(i, folder_path=root, flag=False)
                    big_images = np.concatenate((big_images, image))
            return big_images
        else:
            return False
    except:
        return False

def get_area_total(big_images,mask):
    print(calculate_area(big_images, mask))
    unique_values, counts = np.unique(mask, return_counts=True)
    print(unique_values, counts)
    total_sum = sum(calculate_area(big_images, mask).values())
    return total_sum

def sub(image: np.ndarray,x1:int, y1:int, x2:int, y2:int)-> np.ndarray:
    submatrix = [row[x1:x2] for row in image[y2:y1]]
    resized_submatrix = np.resize(submatrix,(y1 - y2, x2 - x1))
    return resized_submatrix
