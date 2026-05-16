#!/usr/bin/env python3
"""
任务1：将数据集上传至阿里云 OSS
"""

import oss2
from config import (
    ACCESS_KEY_ID, ACCESS_KEY_SECRET, ENDPOINT,
    BUCKET_NAME, OBJECT_KEY, LOCAL_FILE_PATH
)


def get_bucket():
    """获取 Bucket 实例"""
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    return oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)


def create_bucket_if_not_exists(bucket):
    """如果 Bucket 不存在则创建"""
    try:
        bucket.create_bucket(
            oss2.BUCKET_ACL_PRIVATE,  # 私有权限
            oss2.models.BucketCreateConfig(
                storage_class=oss2.BUCKET_STORAGE_CLASS_STANDARD
            )
        )
        print(f"Bucket '{BUCKET_NAME}' 创建成功")
    except oss2.exceptions.BucketAlreadyExists:
        print(f"Bucket '{BUCKET_NAME}' 已存在")
    return bucket


def upload_file(bucket):
    """上传本地文件到 OSS"""
    import os
    if not os.path.exists(LOCAL_FILE_PATH):
        raise FileNotFoundError(f"本地文件不存在: {LOCAL_FILE_PATH}")

    # 上传文件
    bucket.put_object_from_file(OBJECT_KEY, LOCAL_FILE_PATH)
    print(f"   上传成功")
    print(f"   本地文件: {LOCAL_FILE_PATH}")
    print(f"   云端路径: oss://{BUCKET_NAME}/{OBJECT_KEY}")


def verify_upload(bucket):
    """验证上传结果"""
    meta = bucket.head_object(OBJECT_KEY)
    print(f"\n 验证信息:")
    print(f"   文件大小: {meta.content_length:,} bytes ({meta.content_length / 1024 / 1024:.2f} MB)")
    print(f"   最后修改: {meta.last_modified}")
    print(f"   ETag: {meta.etag}")


def main():
    print("=" * 50)
    print("阿里云 OSS 数据集上传")
    print("=" * 50)

    # 获取 bucket
    bucket = get_bucket()

    # 创建 bucket（如不存在）
    create_bucket_if_not_exists(bucket)

    # 上传文件
    upload_file(bucket)

    # 验证
    verify_upload(bucket)

    print("\n" + "=" * 50)
    print("上传完成！可在报告中引用上述验证信息")
    print("=" * 50)


if __name__ == '__main__':
    main()