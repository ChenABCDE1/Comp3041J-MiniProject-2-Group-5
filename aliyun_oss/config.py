import os

ACCESS_KEY_ID = os.environ.get('ALIYUN_ACCESS_KEY_ID', 'placeholder-id')
ACCESS_KEY_SECRET = os.environ.get('ALIYUN_ACCESS_KEY_SECRET', 'placeholder-secret')

# 地域配置
REGION = 'cn-beijing'
ENDPOINT = f'https://oss-{REGION}.aliyuncs.com'

# Bucket 配置
BUCKET_NAME = 'comp3041j-logdata-2026'

# 对象路径
OBJECT_KEY = 'datasets/Comp3041J MiniProject 2 Dataset.csv'
LOCAL_FILE_PATH = 'data/Comp3041J MiniProject 2 Dataset.csv'