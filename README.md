# Mini-Project 2: Cloud Service Log Analytics

## Overview

This project implements a cloud service log analytics pipeline using cloud object storage, MapReduce, and Ray. The workflow follows:

```text
dataset → cloud object storage → MapReduce baseline analytics → Ray extension analytics → comparison
```

---

## Technologies

- **Cloud Storage**: Alibaba Cloud OSS
- **Batch Processing**: Hadoop Streaming MapReduce (3 jobs)
- **Parallel Processing**: Ray (degraded service detection)
- **Validation**: Manual cross-verification scripts

---

## Prerequisites

Install required dependencies:

```bash
pip install -r requirements.txt
```

Required packages:

- oss2
- ray
- pandas

---

## Configuration

Before running the project, configure Alibaba Cloud credentials in:

```python
aliyun_oss/config.py
```

Example configuration:

```python
ACCESS_KEY_ID = 'your-access-key-id'
ACCESS_KEY_SECRET = 'your-access-key-secret'
REGION = 'cn-beijing'  # or your bucket region
BUCKET_NAME = 'your-bucket-name'
```

> Warning:
> Replace placeholders with real credentials for local execution.
> Revert them back before committing to version control.

---

# Task 1: Cloud Object Storage

Upload dataset to Alibaba Cloud OSS:

```bash
cd aliyun_oss
python upload_dataset.py
```

Verify storage:

```bash
python verify_storage.py
```

---

# Task 2: MapReduce Baseline Analytics

Run all three MapReduce jobs:

```bash
cd mapreduce
python run_all.py
```

## Individual Jobs

### Job 1: Request Count by Service

```bash
python job1_request_count/run.py
```

### Job 2: Server Error Count by Service

```bash
python job2_error_count/run.py
```

### Job 3: Top 10 Slow Endpoints

```bash
python job3_slow_endpoints/run.py
```

## Outputs

Results are saved in:

```text
mapreduce/outputs/
```

Generated files:

- `request_count.txt`
- `error_count.txt`
- `top10_slow_endpoints.txt`

---

# Task 3: Ray Degraded Service Detection

Run Ray parallel detection:

```bash
cd ray_detection
python degraded_service_detection.py
```

## Output

Result file:

```text
ray_detection/outputs/degraded_services.txt
```

## Key Implementation

Uses the `@ray.remote` decorator for parallel chunk processing with 4 local CPUs.

---

# Task 4: Validation

Cross-verify all outputs against manual ground-truth counts:

```bash
cd validation
python manual_validation.py
```

## Validation Includes

- Job 1: Request count accuracy
- Job 2: Error count accuracy
- Job 3: Top 10 slow endpoints ranking
- Ray: Degraded service classification correctness

---

# Execution Environments

| Component      | Environment                                |
|----------------|--------------------------------------------|
| MapReduce      | Local Windows Machine                      |
| Ray            | Local Windows Machine, 4 CPUs, Ray 2.10.0 |
| Object Storage | Alibaba Cloud OSS                          |

---
# License

Academic project for COMP3041J Cloud Computing Module.