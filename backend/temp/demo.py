import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from flask import Flask, jsonify, request
from flask_cors import CORS

from render_report import *

app = Flask(__name__)
CORS(app)

def merge_large_img():
    folder_path = "./animation"
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
    return big_images


def get_area_total():
    print(calculate_area(big_images, mask))
    unique_values, counts = np.unique(mask, return_counts=True)
    print(unique_values, counts)
    total_sum = sum(calculate_area(big_images, mask).values())
    return total_sum


def sub(image: np.ndarray,x1:int, y1:int, x2:int, y2:int)-> np.ndarray:
    submatrix = [row[x1:x2] for row in image[y2:y1]]
    resized_submatrix = np.resize(submatrix,(y1 - y2, x2 - x1))
    return resized_submatrix
    
@app.route('/get_area', methods=['GET'])
def get_area():
    params = request.args.to_dict()
    if params:
        data = {key: int(value) for key, value in params.items()}
        img = sub(image=big_images, x1=data['x1'], y1=data['y1'],x2=data['x2'],y2=data['y2'])
        new_models = sub(image=new_mask, x1=data['x1'], y1=data['y1'],x2=data['x2'],y2=data['y2'])  
        
        area = calculate_area(image=img, mask=new_models)
        print(area)
        return jsonify({"img":img.tolist(), 'area': str(area)})
    else:
        return "Successfull Start!"


mask = np.load('C:\\Users\\tuan\\Downloads\\Backend_Func-20240408T145835Z-001\\FinalProject\\backend\\temp\\mask.npy')
new_mask = np.rot90(mask, k=1)
big_images = merge_large_img()
big_images[new_mask == False] = 0

if __name__=="__main__":
    app.run(debug=True)