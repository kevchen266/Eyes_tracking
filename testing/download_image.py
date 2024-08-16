import requests
import os

def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"图像已保存到 {save_path}")
    else:
        print(f"从 {url} 下载图像失败，状态码：{response.status_code}")

# 保存图像的目录
save_directory = "../images"

# 如果目录不存在，则创建目录
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# 下载多个随机人脸图像
for i in range(30):  # 修改范围以获取所需数量的图像
    image_url = f"https://randomuser.me/api/portraits/men/{i % 100}.jpg"  # 生成随机的男头像
    save_path = os.path.join(save_directory, f"image_{i+1}.jpg")
    download_image(image_url, save_path)