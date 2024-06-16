import json
import requests
import numpy as np
import matplotlib.pyplot as plt



def process_path(text: str):
    parts = text.split('/')
    if parts[-1] == "":
        parts = parts[:-1]
    return parts[-3], parts[-2], parts[-1]


def download_satellite_image():
    """Send ward params to download"""
 
    url = 'http://127.0.0.1:5000/download_img'
    params = {
        'province': 'Lâm Đồng',
        'district': 'Đà Lạt',
        'ward':"6",
        'lst_img': []
    }
    # params = {
    #     'province': 'Hồ Chí Minh city',
    #     'district': 'Quận 1',
    #     'ward':"Nguyễn Cư Trinh",
    #     'lst_img': []
    # }
    # params = {
    #     'province': 'Lâm Đồng',
    #     'district': 'Đà Lạt',
    #     'ward':"12",
    #     'lst_img': []
    # }
    response = requests.post(url, params=params)
    try:
        data = json.loads(response.content)
        print(data)
    except:
        data = response.content
        print(data)

def calculate_area():
    """
    Send params to calculate area
    """
    url = 'http://127.0.0.1:5000/get_area'
    # params = {
    #     'province': 'Lâm Đồng',
    #     'district': 'Đà Lạt',
    #     'ward':"12"
    # }
    
    params = {
        'province': 'Lâm Đồng',
        'district': 'Đà Lạt',
        'ward':"6"
    }
    response = requests.post(url, params=params)
    try:
        data = json.loads(response.content)
        area = data['area']
        area_dict = eval(area)
        # plt.imshow(img, cmap='viridis')
        # plt.colorbar()
        # plt.show()
        print(area_dict)
    except:
        data = response.content
        print(data)



def custom_calculate_area():
    """
    Send params to calculate area
    """
    url = 'http://127.0.0.1:5000/get_area'

    annotations = "data/annotation/Lâm Đồng/Đà Lạt/6"
    province, district, ward = process_path(text=annotations)

    # dont wanna change, just comment mask
    mask = "data/mask/Lâm Đồng/Đà Lạt/6"
    province_mask, district_mask, ward_mask = process_path(text=mask)

    params = {
        'province': province,
        'district': district,
        'ward': ward,
        'province_mask': province_mask,
        'district_mask': district_mask,
        'ward_mask': ward_mask
    }
    response = requests.post(url, params=params)
    try:
        data = json.loads(response.content)
        area = data['area']
        area_dict = eval(area)
        print(area_dict)
    except:
        data = response.content
        print(data)


if __name__=="__main__":
    custom_calculate_area()