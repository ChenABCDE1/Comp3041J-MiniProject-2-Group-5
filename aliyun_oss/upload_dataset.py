#!/usr/bin/env python3
"""
Task 1: Upload the data set to OSS in Alibaba Cloud.
"""

import oss2
from config import (
    ACCESS_KEY_ID, ACCESS_KEY_SECRET, ENDPOINT,
    BUCKET_NAME, OBJECT_KEY, LOCAL_FILE_PATH
)


def get_bucket():
    """Get Bucket instance"""
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    return oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)


def create_bucket_if_not_exists(bucket):
    """Create Bucket if it does not exist."""
    try:
        bucket.create_bucket(
            oss2.BUCKET_ACL_PRIVATE,  # BUCKET_ACL_PRIVATE!!!!!!
            oss2.models.BucketCreateConfig(
                storage_class=oss2.BUCKET_STORAGE_CLASS_STANDARD
            )
        )
        print(f"Bucket '{BUCKET_NAME}' Created successfully.")
    except oss2.exceptions.BucketAlreadyExists:
        print(f"Bucket '{BUCKET_NAME}' exist")
    return bucket


def upload_file(bucket):
    """Upload local files to OSS"""
    import os
    if not os.path.exists(LOCAL_FILE_PATH):
        raise FileNotFoundError(f"The local file does not exist: {LOCAL_FILE_PATH}")

    # upload file
    bucket.put_object_from_file(OBJECT_KEY, LOCAL_FILE_PATH)
    print(f"   upload successfully")
    print(f"   local file: {LOCAL_FILE_PATH}")
    print(f"   cloud path: oss://{BUCKET_NAME}/{OBJECT_KEY}")


def verify_upload(bucket):
    """Verify the upload results"""
    meta = bucket.head_object(OBJECT_KEY)
    print(f"\n Authentication information:")
    print(f"   file size: {meta.content_length:,} bytes ({meta.content_length / 1024 / 1024:.2f} MB)")
    print(f"   last modified: {meta.last_modified}")
    print(f"   ETag: {meta.etag}")


def main():
    print("=" * 50)
    print("Alibaba Cloud OSS dataset upload")
    print("=" * 50)

    # get bucket
    bucket = get_bucket()

    # create bucket（如不存在）
    create_bucket_if_not_exists(bucket)

    # upload file
    upload_file(bucket)

    # verify
    verify_upload(bucket)

    print("\n" + "=" * 50)
    print("finish")
    print("=" * 50)


if __name__ == '__main__':
    main()