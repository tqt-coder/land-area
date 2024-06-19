import torch
import matplotlib.pyplot as plt
from mmengine.model.utils import revert_sync_batchnorm
from mmseg.apis import init_model, inference_model, show_result_pyplot
config_file = 'C:/Users/tuan/Downloads/aa/mmcv/mmsegmentation/configs/segformer/segformer_mit-b5_8xb2-160k_loveda-640x640.py'
checkpoint_file = 'C:/Users/tuan/Downloads/segformer.pth'
# build the model from a config file and a checkpoint file

import os


def create_inference(province, district, ward):
    try:
        if not torch.cuda.is_available():
            model = init_model(config_file, checkpoint_file, device='cpu')
            model = revert_sync_batchnorm(model)
            current_dir = os.getcwd()

            folder_path = os.path.join(current_dir, 'data', 'images', province, district, ward)
            print(folder_path)
            # folder_path = 'str_url_annotations'
            for filename in os.listdir(folder_path):
                image_path = os.path.join(folder_path, filename)
                # print(filename)
                # folder_name = 'Phuong 12'
                result = inference_model(model, image_path)
                str_url = os.path.join(current_dir, 'data', 'annotations', province, district, ward)
                savedir = f'{str_url}/'
                vis_iamge = show_result_pyplot(model, image_path, result, save_dir =savedir ,out_file =savedir + filename,
                                                opacity=1.0, show=False,  draw_gt=True, with_labels=False)
        print(str_url)
        return str_url
    except Exception as e:
        print(str(e))
        return str(e)