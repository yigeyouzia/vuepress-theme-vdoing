from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import os

# 读取配置文件
with open("cos.conf", "r") as f:
    config = f.readlines()
    print("配置参数config", config)
secret_id = config[0].strip()
secret_key = config[1].strip()
region = config[2].strip()
bucket_name = config[3].strip()

# 初始化COS客户端
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
client = CosS3Client(config)


# 上传文件到COS
def upload_all():
    # 上传dist目录下的所有文件和文件夹
    print("开始上传文件...")
    for root, dirs, files in os.walk("./docs/.vuepress/dist"):
        for file in files:
            file_path = os.path.join(root, file)
            file_name = os.path.relpath(file_path, "./docs/.vuepress/dist")
            file_path = file_path.replace(os.sep, "/")
            file_name = file_name.replace(os.sep, "/")
            print(file_path)
            print(file_name)
            with open(file_path, "rb") as fp:
                response = client.put_object(Bucket=bucket_name, Body=fp, Key=file_name)
                print(response["ETag"])
                print(f"Uploaded {file_path} to {bucket_name}/{file_name}")


def delette_all():
    # 列出存储桶中的所有对象
    response = client.list_objects(Bucket=bucket_name)
    print("删除...")
    # 遍历所有对象并删除
    for content in response.get("Contents", []):
        key = content["Key"]
        print(f"Deleting {key}...")
        response = client.delete_object(Bucket=bucket_name, Key=key)
        print(response)

    print("删除完毕.")


if __name__ == "__main__":
    print("连接测试...", client)
    # delette_all()
    upload_all()
