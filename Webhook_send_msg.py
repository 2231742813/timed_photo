import requests
import base64
import hashlib
import os
from PIL import Image
from Read_Phone_Camera_Config import Read_Phone_Camera_Config

data = Read_Phone_Camera_Config()
target_folder = data['target_folder']
Wenhook_url = data['Webhook_url']
Wenhook_url_1 = data['Wenhook_url_1']


# 必须与图片服务器在一个局域网下才能查看图片
def Wenhook_send(picture_name, titles='默认标题', descriptions='默认描述'):
    # API URL

    # 请求体数据
    datas = {
        "msgtype": "news",
        "news": {
            "articles": [
                {
                    "title": titles,
                    "description": descriptions,
                    "url": target_folder + picture_name,
                    "picurl": target_folder + picture_name,
                }
            ]
        }
    }

    # 发送请求
    response = requests.post(url=Wenhook_url, json=datas)
    print("需在同一局域网下查看图片")
    print(response.text)


# 企业微信直接推送图片，但要小于2M所以对图片进行压缩
def load_image(file_path):
    # 图片路径
    picture_url = target_folder
    # 图片路径+图片名称
    file_path = picture_url + file_path
    # 获取文件大小
    file_size = os.path.getsize(file_path)

    # 如果文件大小小于 1.8M，直接读取
    if file_size <= 1.8 * 1024 * 1024:
        with open(file_path, 'rb') as f:
            image_data = f.read()
    else:
        # 如果文件大小大于 1.8M，压缩至小于 1.8M 后读取
        max_size = 1.8 * 1024 * 1024
        output_file = 'compressed.jpg'
        with Image.open(file_path) as im:
            im.thumbnail((1024, 1024))
            im.save(output_file, optimize=True, quality=85)
            while os.path.getsize(output_file) > max_size:
                im = im.resize((int(im.width * 0.9), int(im.height * 0.9)), resample=Image.LANCZOS)
                im.save(output_file, optimize=True, quality=85)

        with open(output_file, 'rb') as f:
            image_data = f.read()

    return image_data

# 压缩后直接展示在企业微信，有网即可查看
def Wenhook_send_1(picture_name):
    # API URL
    url = Wenhook_url_1
    picture_data = load_image(picture_name)
    base64_data = base64.b64encode(picture_data).decode('utf-8')
    md5_value = hashlib.md5(picture_data).hexdigest()
    # 请求体数据
    datas = {
        "msgtype": "image",
        "image": {
            "base64": base64_data,
            "md5": md5_value,
            "pic_url": ""
        }
    }

    # 发送请求
    response = requests.post(url=url, json=datas)
    print("企业微信直接查看图片")
    print(response.text)

