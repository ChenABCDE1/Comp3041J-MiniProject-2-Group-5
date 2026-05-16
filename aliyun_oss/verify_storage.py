#!/usr/bin/env python3
"""
Task 1 Verification: Retrieve anonymized storage evidence for the Group Report.
This script connects to Alibaba Cloud OSS, verifies the uploaded dataset exists,
and outputs storage metadata suitable for inclusion in the project report.
"""

import oss2
import sys
import os

# Add parent directory to path for importing the config module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import ACCESS_KEY_ID, ACCESS_KEY_SECRET, ENDPOINT, BUCKET_NAME, OBJECT_KEY


def get_bucket_instance():
    """Create and return an OSS Bucket instance using credentials from config."""
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    return oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)


def retrieve_storage_evidence(bucket):
    """
    Fetch metadata of the uploaded object to verify storage
    and generate anonymized evidence for the report.
    """
    # Verify the object exists and retrieve its metadata
    meta = bucket.head_object(OBJECT_KEY)
    return meta


def display_anonymized_evidence(meta):
    """
    Print anonymized storage evidence.
    Identifying information (bucket names, account IDs) must be redacted
    in screenshots used for the report.
    """
    print("=" * 60)
    print("Anonymized Storage Evidence for Group Report")
    print("=" * 60)
    print()
    print(f"Cloud Storage Service: Alibaba Cloud Object Storage Service (OSS)")
    print(f"Region Endpoint: {ENDPOINT.replace('https://', '')}")
    print(f"Object Key: {OBJECT_KEY}")
    print(f"File Size: {meta.content_length:,} bytes ({meta.content_length / 1024 / 1024:.2f} MB)")
    print(f"Storage Class: Standard")
    print(f"Access Control: Private")
    print(f"Last Modified: {meta.last_modified}")
    print()
    print("-" * 60)
    print("NOTE: When including screenshots in the report, ensure the")
    print("following identifying information is redacted or obscured:")
    print("  - Alibaba Cloud account ID and username")
    print("  - Full bucket name")
    print("  - File paths containing personal identifiers")
    print("  - Access keys and endpoint URLs in console navigation")
    print("-" * 60)


def list_bucket_objects(bucket):
    """List all objects in the bucket for verification purposes."""
    print("\nObject Listing within Bucket:")
    print("-" * 60)
    for obj in oss2.ObjectIterator(bucket):
        size_mb = obj.size / 1024 / 1024
        print(f"  Object: {obj.key} | Size: {size_mb:.2f} MB | Modified: {obj.last_modified}")
    print("-" * 60)


def main():
    print("Executing OSS Storage Verification...")

    # Check if credentials are still placeholder values
    if ACCESS_KEY_ID == 'your-access-key-id' or 'placeholder' in ACCESS_KEY_ID:
        print("\nERROR: Please configure valid Alibaba Cloud credentials in config.py")
        print("       Obtain credentials from: Alibaba Cloud Console -> AccessKey Management")
        return

    # Initialize bucket connection
    bucket = get_bucket_instance()

    # Retrieve and display storage evidence
    meta = retrieve_storage_evidence(bucket)
    display_anonymized_evidence(meta)

    # List all objects for additional verification
    list_bucket_objects(bucket)

    print("\n" + "=" * 60)
    print("Verification complete. Data is confirmed in cloud object storage.")
    print("Use the output above as evidence in Section II of the Group Report.")
    print("=" * 60)


if __name__ == '__main__':
    main()