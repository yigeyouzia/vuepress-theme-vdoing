from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import os

# 初始化COS客户端
secret_id = 'YOUR_SECRET_ID'  # 替换为您的腾讯云COS SecretId
secret_key = 'YOUR_SECRET_KEY'  # 替换为您的腾讯云COS SecretKey
region = 'YOUR_REGION'  # 替换为您的腾讯云COS区域
bucket_name = 'YOUR_BUCKET_NAME'  # 替换为您的腾讯云COS存储桶名称

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
client = CosS3Client(config)

# 上传文件到COS
def upload_file(file_path):
    file_name = os.path.relpath(file_path, './docs/.vuepress/dist')
    response = client.put_object(
        Bucket=bucket_name,
        Body=open(file_path, 'rb'),
        Key=file_name
    )
    print(f"Uploaded {file_path} to {bucket_name}/{file_name}")

# 上传dist目录下的所有文件和文件夹
for root, dirs, files in os.walk('./docs/.vuepress/dist'):
    for file in files:
        file_path = os.path.join(root, file)
        upload_file(file_path)